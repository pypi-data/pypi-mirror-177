#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nallezard.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from ._frontend import module_name, module_version
from ipywidgets.widgets.trait_types import (
    bytes_serialization,
    _color_names,
    _color_hex_re,
    _color_hexa_re,
    _color_rgbhsl_re,
)
from traitlets import (
    Bool,
    Bytes,
    CInt,
    Enum,
    Float,
    Instance,
    List,
    Unicode,
    TraitError,
    Union,
)
from ipydatawidgets import (
    NDArray, array_serialization)
import numpy as np

class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ExampleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    array = NDArray(np.zeros(0)).tag(sync=True, **array_serialization)
    array_out = NDArray(np.zeros(0)).tag(sync=True, **array_serialization)
    model_path=Unicode("./model.onnx").tag(sync=True)
    wasm_path=Unicode("./wasm").tag(sync=True)
    initialized=Bool(False).tag(sync=True)
    done=Bool(False).tag(sync=True)
    value = Unicode('Hello World').tag(sync=True)
    image_data = Bytes(default_value=None, allow_none=True).tag(
        sync=True, **bytes_serialization
    )
    def __init__(self, *args, **kwargs):
        """Create a Canvas widget."""
        super(ExampleWidget, self).__init__(*args, **kwargs)
        print("init widget")