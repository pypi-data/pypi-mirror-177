from .nodes import (
    NapariImageSource,
    NapariLabelsSource,
    OnesSource,
    Binarize,
    NpArraySource,
)

import gunpowder as gp

import numpy as np
from bioimageio.core.resource_io.nodes import Model

from contextlib import contextmanager
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import math

LayerName = str
LayerType = str


@dataclass
class GunpowderParameters:
    gaussian_noise_mean: float = 0.0
    gaussian_noise_var: float = 0.01
    salt_noise: float = 0.02
    pepper_noise: float = 0.02
    elastic_control_point_spacing: int = 50
    elastic_control_point_sigma: int = 10
    downsample_factor: int = 4
    rotation: bool = True
    mirror: bool = True
    transpose: bool = True
    num_cpu_processes: int = 1
    batch_size: int = 4


class PipelineDataGenerator:
    """
    Simple wrapper around a gunpowder pipeline.
    """

    def __init__(
        self,
        pipeline: gp.Pipeline,
        val_pipeline: gp.Pipeline,
        request: gp.BatchRequest,
        val_request: gp.BatchRequest,
        snapshot_request: gp.BatchRequest,
        keys: List[Tuple[gp.ArrayKey, str]],
        axes: List[str],
    ):
        self.pipeline = pipeline
        self.val_pipeline = val_pipeline
        self.request = request
        self.val_request = val_request
        self.snapshot_request = snapshot_request
        self.keys = keys
        self.spatial_axes = axes

    def next(
        self, snapshot: bool
    ) -> Tuple[
        List[Tuple[np.ndarray, Dict[str, Any], LayerType]],
        List[Tuple[np.ndarray, Dict[str, Any], LayerType]],
    ]:
        request = gp.BatchRequest()
        request_template = self.snapshot_request if snapshot else self.request
        for k, v in request_template.items():
            request[k] = v
        batch = self.pipeline.request_batch(request)

        arrays = []
        snapshot_arrays = []
        for key, layer_type in self.keys:
            if key in request_template:
                layer = (
                    batch[key].data,
                    {
                        "name": f"sample_{key}".lower(),
                        "axes": ("batch", "channel", *self.spatial_axes),
                    },
                    layer_type,
                )
                if key in self.request:
                    arrays.append(layer)
                else:
                    snapshot_arrays.append(layer)

        return arrays, snapshot_arrays

    def next_validation(
        self,
    ) -> List[Tuple[np.ndarray, Dict[str, Any], LayerType]]:
        request = gp.BatchRequest()
        request_template = self.val_request
        for k, v in request_template.items():
            request[k] = v
        batch = self.val_pipeline.request_batch(request)

        arrays = []
        for key, layer_type in self.keys:
            if key in request_template:
                layer = (
                    batch[key].data,
                    {
                        "name": f"sample_{key}".lower(),
                        "axes": ("batch", "channel", *self.spatial_axes),
                    },
                    layer_type,
                )
                if key in self.request:
                    arrays.append(layer)

        return arrays


@contextmanager
def build_pipeline(raw, mask, model: Model, parameters: GunpowderParameters):

    outputs = model.outputs
    metadata_output_names = [output.name.lower() for output in outputs]
    output_names = [x for x in metadata_output_names]
    if "pssr" not in output_names:
        output_names[0] = "pssr"
        if len(output_names) > 1:
            raise ValueError(
                f"Don't know how to handle outputs: {metadata_output_names}"
            )
    try:
        pssr_index = output_names.index("pssr")
    except ValueError as e:
        raise ValueError(
            'This model does not provide an output with name "pssr"! '
            f"{model.name} only provides: {output_names}"
        )

    # read metadata from model
    dims = 2
    spatial_axes = ["time", "z", "y", "x"][-dims:]

    input_shape = gp.Coordinate(model.inputs[0].shape.min[-dims:])
    output_shape = gp.Coordinate(input_shape)

    # get voxel sizes TODO: read from metadata?
    voxel_size = gp.Coordinate((1,) * input_shape.dims)

    # switch to world units:
    input_size = voxel_size * input_shape
    output_size = voxel_size * output_shape
    context = (input_size - output_size) / 2

    # padding of groundtruth/mask
    # without padding you random sampling won't be uniform over the whole volume
    padding = output_size

    # define keys:
    raw_key = gp.ArrayKey("RAW")
    crap_key = gp.ArrayKey("CRAPIFIED")
    mask_key = gp.ArrayKey("MASK")
    training_mask_key = gp.ArrayKey("TRAINING_MASK_KEY")

    # Get source nodes:
    raw_source = NapariImageSource(raw, raw_key)
    val_raw_source = NapariImageSource(raw, raw_key)
    # Pad raw infinitely with 0s. This is to avoid failing to train on any of
    # the ground truth because there wasn't enough raw context.

    with gp.build(val_raw_source):
        val_roi = gp.Roi(
            val_raw_source.spec[raw_key].roi.get_offset(), output_size
        )
        total_roi = val_raw_source.spec[raw_key].roi.copy()
        training_mask_spec = val_raw_source.spec[raw_key].copy()

    shape = total_roi.get_shape() / voxel_size
    training_mask = np.ones(shape, dtype=training_mask_spec.dtype)
    val_slices = [
        slice(0, val_shape) for val_shape in val_roi.get_shape() / voxel_size
    ]
    training_mask[tuple(val_slices)] = 0

    training_mask_source = NpArraySource(
        training_mask, training_mask_spec, training_mask_key
    )

    if mask is not None:
        mask_source = NapariLabelsSource(mask, mask_key)
        val_mask_source = NapariLabelsSource(mask, mask_key)
    else:
        with gp.build(raw_source):
            mask_spec = raw_source.spec[raw_key]
            mask_spec.dtype = bool
            mask_source = OnesSource(raw_source.spec[raw_key], mask_key)
            val_mask_source = OnesSource(
                raw_source.spec[raw_key].copy(), mask_key
            )

    # Pad mask with just enough to make sure random sampling is uniform
    mask_source += gp.Pad(mask_key, padding, 0)
    val_mask_source += gp.Pad(mask_key, padding, 0)

    val_pipeline = (val_raw_source, val_mask_source) + gp.MergeProvider()
    pipeline = (
        (raw_source, mask_source, training_mask_source)
        + gp.MergeProvider()
        + gp.RandomLocation(min_masked=1, mask=training_mask_key)
    )
    pipeline += gp.Normalize(raw_key)
    val_pipeline += gp.Normalize(raw_key)

    val_pipeline += gp.Resample(
        raw_key,
        voxel_size * parameters.downsample_factor,
        crap_key,
        interp_order=1,
    )
    val_pipeline += gp.Pad(crap_key, None)
    pipeline += gp.Resample(
        raw_key,
        voxel_size * parameters.downsample_factor,
        crap_key,
        interp_order=1,
    )
    pipeline += gp.Pad(crap_key, None)

    if parameters.mirror or parameters.transpose:
        pipeline += gp.SimpleAugment(
            mirror_only=[1 if parameters.mirror else 0 for _ in range(dims)],
            transpose_only=[
                1 if parameters.transpose else 0 for _ in range(dims)
            ],
        )
    pipeline += gp.NoiseAugment(
        crap_key,
        mean=parameters.gaussian_noise_mean,
        var=parameters.gaussian_noise_var,
        mode="gaussian",
    )
    pipeline += gp.NoiseAugment(
        crap_key,
        amount=parameters.salt_noise,
        mode="salt",
    )
    pipeline += gp.NoiseAugment(
        crap_key,
        amount=parameters.pepper_noise,
        mode="pepper",
    )

    # Trainer attributes:
    if parameters.num_cpu_processes > 1 and False:
        pipeline += gp.PreCache(num_workers=parameters.num_cpu_processes)

    # add channel dimensions
    pipeline += gp.Unsqueeze([raw_key, crap_key, mask_key])
    val_pipeline += gp.Unsqueeze([raw_key, crap_key, mask_key])

    # stack to create a batch dimension
    pipeline += gp.Stack(parameters.batch_size)
    val_pipeline += gp.Stack(1)

    request = gp.BatchRequest()
    request.add(raw_key, input_size)
    request.add(crap_key, output_size)
    request.add(training_mask_key, output_size)

    val_request = gp.BatchRequest()
    val_request[raw_key] = gp.ArraySpec(roi=val_roi.grow(context, context))
    val_request[crap_key] = gp.ArraySpec(roi=val_roi.grow(context, context))

    snapshot_request = gp.BatchRequest()
    snapshot_request.add(raw_key, input_size)
    snapshot_request.add(crap_key, input_size)
    snapshot_request.add(training_mask_key, output_size)
    snapshot_request.add(mask_key, output_size)

    keys = [
        (crap_key, "image"),
        (raw_key, "image"),
        (mask_key, "labels"),
    ]

    with gp.build(pipeline):
        with gp.build(val_pipeline):
            yield PipelineDataGenerator(
                pipeline,
                val_pipeline,
                request,
                val_request,
                snapshot_request,
                keys,
                axes=spatial_axes,
            )
