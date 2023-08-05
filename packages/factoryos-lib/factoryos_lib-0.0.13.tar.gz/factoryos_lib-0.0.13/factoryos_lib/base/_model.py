# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]


import sys
import json

from abc import abstractmethod

from ValiotWorker.worker import JobStatus
from ValiotWorker.Logging import LogLevel

from factoryos_lib.base._component import Component


class Model(Component):
    """ Model
           Overview:
           - Abstract class to define a reusable model
           Parameters
           ----------
           model_name : name of the model
           controller_model_json : json structure for the model
           controller_output_alert_id :
           feedback_alert_id :

       """

    def __init__(self):
        super().__init__()


    def execute(self, job, log, update_job):
        log(LogLevel.DEBUG, '{} Base Model is running ...'.format(job["queue"]["name"]))
        update_job({'status': JobStatus.RUNNING, 'progress': 0})

        try:
            # Initialize Executor Object.
            self.initialize(job, log)

            # Gets the model from Valiot DB.
            self.get_model_from_db()

            # Build the Neural Network according with the Model.
            self.build_model()

            # Gets & Normalizes Inputs.
            self.inputs_preprocess()

            # Forecast the outpus.
            self.predict()

            # Post the outputs.
            self.post_solution()

            # Update job status to complete.
            update_job({
                'status': JobStatus.FINISHED,
                'output': json.dumps({'output': 'Successful', 'errors': ''})
            })

        # Make exception case for error handling
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            log(LogLevel.ERROR, 'Some error with {}...'.format(
                job["queue"]["name"]))
            log(LogLevel.ERROR,
                f'{e}, file: {exc_tb.tb_frame.f_code.co_filename}, line: {exc_tb.tb_lineno}')
            update_job({
                'status': JobStatus.ERROR,
                'output': json.dumps({'output': 'Error',
                                      'errors': f'{e}',
                                      'file': f'{exc_tb.tb_frame.f_code.co_filename}',
                                      'line': f'{exc_tb.tb_lineno}'
                                      })
            })

    @abstractmethod
    def initialize(self, job, log):
        pass

    @abstractmethod
    def get_model_from_db(self):
        pass

    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def inputs_preprocess(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def post_solution(self):
        pass
