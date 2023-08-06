from __future__ import annotations

import torch
from scipy.optimize import linear_sum_assignment
from torchvision.ops import generalized_box_iou


def classification_cost(
    pred_logits: torch.Tensor,
    gt_labels: torch.Tensor,
    alpha: float = 0.25,
    gamma: float = 2.0,
) -> torch.Tensor:
    """Compute focal loss cost for matching."""
    probs = torch.sigmoid(pred_logits)
    neg_cost_class = (1 - alpha) * (probs**gamma) * -torch.log(1 - probs + 1e-8)
    pos_cost_class = alpha * ((1 - probs) ** gamma) * -torch.log(probs + 1e-8)
    return pos_cost_class[:, gt_labels] - neg_cost_class[:, gt_labels]


def match_targets(
    targets: list[dict[str, torch.Tensor]],
    outputs: dict[str, torch.Tensor],
    anchors: torch.Tensor,
    n_anchors_per_level: list[int],
) -> list[torch.Tensor]:
    """Match targets and predictions 1:1."""
    matched_idxs = []
    for pred_boxes, pred_logits, target in zip(
        outputs["boxes"], outputs["logits"], targets
    ):
        matched_idx = -torch.ones(len(pred_boxes)).long()
        if target["boxes"].numel() == 0:
            matched_idxs.append(matched_idx)
            continue

        # Require matched ground truth boxes to be within anchor center radii
        gt_boxes = target["boxes"]
        gt_centers = (gt_boxes[:, :2] + gt_boxes[:, 2:]) / 2  # Nx2
        anchor_centers = (anchors[:, :2] + anchors[:, 2:]) / 2  # N
        anchor_sizes = anchors[:, 2] - anchors[:, 0]
        # center sampling: anchor point must be close enough to gt center.
        pairwise_match = (
            anchor_centers[:, None, :] - gt_centers[None, :, :]
        ).abs_().max(dim=2).values < 1.5 * anchor_sizes[:, None]
        # compute pairwise distance between N points and M boxes
        x, y = anchor_centers.unsqueeze(dim=2).unbind(dim=1)  # (N, 1)
        x0, y0, x1, y1 = gt_boxes.unsqueeze(dim=0).unbind(dim=2)  # (1, M)
        pairwise_dist = torch.stack([x - x0, y - y0, x1 - x, y1 - y], dim=2)  # (N, M)

        # anchor point must be inside gt
        pairwise_match &= pairwise_dist.min(dim=2).values > 0

        # each anchor is only responsible for certain scale range.
        lower_bound = anchor_sizes * 4
        lower_bound[: n_anchors_per_level[0]] = 0
        upper_bound = anchor_sizes * 8
        upper_bound[-n_anchors_per_level[-1] :] = torch.inf
        pairwise_dist = pairwise_dist.max(dim=2).values
        pairwise_match &= (pairwise_dist > lower_bound[:, None]) & (
            pairwise_dist < upper_bound[:, None]
        )
        class_cost = classification_cost(pred_logits, target["labels"])
        giou_cost = 1 - generalized_box_iou(pred_boxes, target["boxes"])
        cost = pairwise_dist + class_cost + giou_cost
        cost[~pairwise_match] = torch.inf
        try:
            anchor_indices, gt_indices = linear_sum_assignment(cost.detach().cpu())
        except ValueError:
            matched_idxs.append(matched_idx)
            continue
        matched_idx[anchor_indices] = torch.from_numpy(gt_indices)
        matched_idxs.append(matched_idx)

    return matched_idxs
