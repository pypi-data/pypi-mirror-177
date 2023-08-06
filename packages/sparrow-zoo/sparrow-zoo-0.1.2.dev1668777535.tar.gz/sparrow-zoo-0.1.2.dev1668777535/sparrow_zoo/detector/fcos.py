"""FCOS object detector."""
from __future__ import annotations

from collections import OrderedDict
from typing import Callable, Optional

import torch
from torchvision.models import ResNet, resnet18, resnet50
from torchvision.models.detection import FCOS as _FCOS
from torchvision.models.detection.anchor_utils import AnchorGenerator
from torchvision.models.detection.backbone_utils import LastLevelMaxPool
from torchvision.models.detection.image_list import ImageList
from torchvision.models.feature_extraction import create_feature_extractor

from .base import SparrowDetector
from .box_ops import decode_box_offsets
from .fpn import FeaturePyramidNetwork
from .matcher import match_targets

_BACKBONE: dict[str, Callable[..., ResNet]] = {
    "resnet18": resnet18,
    "resnet50": resnet50,
}


class _FCOSBackbone(torch.nn.Module):
    def __init__(self, backbone: ResNet, out_channels: int) -> None:
        super().__init__()
        self.nodes = [f"layer{num}" for num in [1, 2, 3, 4]]
        self.backbone = create_feature_extractor(
            backbone, {name: name for name in self.nodes}
        )

        with torch.no_grad():
            _features = self.feature_list(self.backbone(torch.randn((1, 3, 1, 512))))
            self.input_channels = [_f.shape[1] for _f in _features]
            self.strides = [512 / _f.shape[-1] for _f in _features]
        self.out_channels = out_channels
        self.fpn = FeaturePyramidNetwork(
            self.input_channels,
            out_channels,
            extra_blocks=LastLevelMaxPool(),
        )
        # Add stride for extra_block
        self.strides.append(self.strides[-1] / 2)

    def feature_list(self, x: dict[str, torch.Tensor]) -> list[torch.Tensor]:
        return [x[name] for name in self.nodes]

    def forward(self, x: torch.Tensor) -> list[torch.Tensor]:
        features = self.feature_list(self.backbone(x))
        return self.fpn(features)


class FCOS(SparrowDetector):
    def __init__(
        self,
        n_classes: int,
        backbone_name: str = "resnet50",
        fpn_out_channels: int = 256,
    ) -> None:
        super().__init__()
        self.n_classes = n_classes
        backbone: ResNet = _BACKBONE[backbone_name](weights="IMAGENET1K_V2")
        self.backbone = _FCOSBackbone(backbone, fpn_out_channels)
        anchor_generator = AnchorGenerator(self.backbone.strides, (1,))
        self.anchors: Optional[torch.Tensor] = None
        self.n_anchors_per_level: Optional[list[int]] = None
        self._fcos = _FCOS(
            self.backbone,
            n_classes,
            anchor_generator=anchor_generator,
        )

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        features: list[torch.Tensor] = self.backbone(x)
        logits = self._fcos.head.classification_head(features)
        box_offsets, centerness = self._fcos.head.regression_head(features)
        if self.anchors is None:
            (self.anchors,) = self._fcos.anchor_generator(
                ImageList(x, [x.shape[-2:]]), features
            )
        if self.n_anchors_per_level is None:
            self.n_anchors_per_level = [x.size(2) * x.size(3) for x in features]
        boxes = decode_box_offsets(box_offsets, self.anchors)
        scores, labels = torch.max(torch.sigmoid(logits), dim=-1)
        return OrderedDict(
            boxes=boxes,
            scores=scores,
            labels=labels,
            logits=logits,
            box_offsets=box_offsets,
            centerness=centerness,
        )

    def compute_detector_loss(
        self, targets: list[dict[str, torch.Tensor]], outputs: dict[str, torch.Tensor]
    ) -> dict[str, torch.Tensor]:
        """Compute 1:1 FCOS loss."""
        matched_indices = match_targets(
            targets, outputs, self.anchors, self.n_anchors_per_level
        )
        head_outputs = dict(
            cls_logits=outputs["logits"],
            bbox_regression=outputs["box_offsets"],
            bbox_ctrness=outputs["centerness"],
        )
        losses = self._fcos.head.compute_loss(
            targets,
            head_outputs,
            [self.anchors] * len(targets),
            matched_indices,
        )
        return {
            "classification": losses["classification"],
            "regression": losses["bbox_regression"],
            "centerness": losses["bbox_ctrness"],
        }
