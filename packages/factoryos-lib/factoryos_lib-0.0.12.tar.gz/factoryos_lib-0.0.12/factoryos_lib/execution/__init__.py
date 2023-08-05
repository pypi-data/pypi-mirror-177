# Copyright 2022 Valiot. | All Rights Reserved

"""Base classes for defining structure of workers."""

__author__ = ["alejandro.pasos@valiot.io"]
__all__ = [
    "setup_gql",
    "execute_jobs"
]

from factoryos_lib.execution.config import setup_gql
from factoryos_lib.execution.execute_jobs import execute_jobs
