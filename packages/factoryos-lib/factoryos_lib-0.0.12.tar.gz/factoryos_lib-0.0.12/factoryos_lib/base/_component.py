# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["alejandro.pasos@valiot.io"]



from abc import ABC, abstractmethod


class Component(ABC):
    """ Component
        Overview:
        - Base structure for the algorithm components
        Parameters
        ----------
        log_callback : referrnce for the log function
        job_name : string

    """    

    def __init__(self):
        self.log_callback = None
        self.job_name = None

    def initialize(self, job, log, __, context, update_context):
        self.log_callback = log
        self.job_name = job["queue"]["name"]


    @abstractmethod
    def execute(self, job, log, update_job, get_job_status, context, update_context, **kwargs):
        pass