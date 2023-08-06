from __future__ import annotations

import abc
import subprocess
import tempfile
from pathlib import Path
from typing import TypeVar, Union

import torch

T = TypeVar("T", bound="SparrowModel")


class SparrowModel(torch.nn.Module):
    """Base model class with useful methods defined."""

    @property
    @abc.abstractmethod
    def output_names(self) -> tuple[str, ...]:
        """Keys in result dict."""
        raise NotImplementedError

    @abc.abstractmethod
    def forward(self, x: torch.Tensor) -> Union[torch.Tensor, dict[str, torch.Tensor]]:
        """
        Run a forward pass.

        Parameters
        ----------
        x
            A ``(batch_size, n_channels, n_rows, n_cols)`` input tensor

        Returns
        -------
        result
            A result tensor or a dictionary with string keys and tensor values
        """
        raise NotImplementedError

    def save(self, path: Union[Path, str]) -> None:
        """
        Save model weights to file.

        Parameters
        ----------
        path
            The location for saving the weights file
        """
        torch.save(self.state_dict(), path)

    def load(self, path: Union[Path, str]) -> None:
        """
        Load model weights from disk.

        Parameters
        ----------
        path
            The location of the weights file
        """
        model_keys = set(self.state_dict().keys())
        new_state_dict = torch.load(path)
        new_keys = set(new_state_dict.keys())
        for key in new_keys - model_keys:
            del new_state_dict[key]
        self.load_state_dict(new_state_dict, strict=False)

    def export(
        self,
        path: Union[Path, str],
        input_shape: tuple[int, ...],
    ) -> None:
        """
        Export the model to ONNX.

        Parameters
        ----------
        path
            The path for saving the file
        input_shape
            The shape to support
        """
        path = Path(path)
        x = torch.randn(*input_shape)
        training = self.training
        self.eval()
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / path.name
            torch.onnx.export(
                self,
                x,
                tmp_path,
                input_names=["input"],
                output_names=self.output_names,
            )
            code = subprocess.call(
                [
                    "polygraphy",
                    "surgeon",
                    "sanitize",
                    tmp_path,
                    "--fold-constants",
                    "-o",
                    path,
                ]
            )
            assert code == 0, "Export failed. Try re-running with debug=True."
        if training:
            self.train()

    def export_tensorrt(
        self,
        path: Union[Path, str],
        input_shape: tuple[int, ...],
        debug: bool = False,
    ) -> None:
        """
        Export the model to TensorRT.

        Parameters
        ----------
        path
            The path for saving the file
        input_shape
            The shape to support
        """
        import tensorrt as trt

        assert str(path).endswith(".engine"), "Path must have a .engine suffix"
        engine_path = Path(path)
        engine_path.parent.mkdir(parents=True, exist_ok=True)
        onnx_path = engine_path.parent / engine_path.name.replace(".engine", ".onnx")
        self.export(onnx_path, input_shape)
        kwargs = dict()
        if not debug:
            kwargs["stdout"] = subprocess.DEVNULL
        logger = trt.Logger(trt.Logger.INFO if debug else trt.Logger.ERROR)
        builder = trt.Builder(logger)
        config = builder.create_builder_config()
        network = builder.create_network()
        flag = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        network = builder.create_network(flag)
        parser = trt.OnnxParser(network, logger)
        assert parser.parse_from_file(str(onnx_path)), "Failed to parse ONNX file."
        engine = builder.build_serialized_network(network, config)
        with open(engine_path, "wb") as f:
            f.write(engine)
