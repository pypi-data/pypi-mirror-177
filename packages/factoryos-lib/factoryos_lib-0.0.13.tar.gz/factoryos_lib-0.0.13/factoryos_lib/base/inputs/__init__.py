# Copyright 2022 Valiot. | All Rights Reserved

""" Define the components for a reusable neural network model."""

__author__ = ["alejandro.pasos@valiot.io"]
__all__ = [

    "ManualInput",
    "VariableInput",
    "AllVariableInput"
]

from factoryos_lib.base.inputs._manual import ManualInput
from factoryos_lib.base.inputs._variable import VariableInput
from factoryos_lib.base.inputs._all_variable import AllVariableInput
