# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]

import os
import sys
import json
import pydash as __
from abc import abstractmethod

from ValiotWorker import JobStatus
from ValiotWorker.Logging import LogLevel

from factoryos_lib.base._component import Component

AWS_ENDPOINT = os.environ.get('AWS_ENDPOINT')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')


class Trainer(Component):
    """ Trainer
               Overview:
               - Abstract class to define trainer for a model
               Parameters
               ----------
               TBD

           """

    def __init__(self):
        super().__init__()

        # Defined on initialize
        self.update_context_callback = None
        self.queue_context = None  # invoked on get_old_and_new_td
        self.queue_obj = None  # invoked on get_old_and_new_td
        self.client = None
        self.controller_model_json = None
        self.training_data_size = None  # invoked on get_old_and_new_td
        self.validation_parameters = None  # invoked on get_old_and_new_td

        # Defined on get_old_and_new_td
        self.current_cursor = None
        self.old_cursor = None
        self.old_prediction_loss = None
        self.next_cursor = None
        self.new_td = None  # invoked on validate_td_size
        self.old_td = None
        self.vd_batch = None

        # Defined on td_preprocess
        self.old_training_inputs = None
        self.old_training_outputs = None
        self.training_outputs = None
        self.training_inputs = None
        self.validation_outputs = None
        self.validation_inputs = None

        self.new_model = None

    @abstractmethod
    def initialize(self, job, log, queue_info, context, update_context):
        pass

    def execute(self, job, log, update_job, get_job_status, context, update_context):
        log(LogLevel.DEBUG, 'Trainer {} is running ...'.format(job["queue"]["name"]))
        update_job({'status': JobStatus.RUNNING,
                    'progress': 0})
        try:
            # Initialize Trainer with the model data.
            self.initialize(job, log, __, context, update_context)

            # Get Old & New TD from .
            self.get_old_and_new_td()

            # Validate if the TD is ready.
            if not self.validate_td_size(update_job):
                # The TD is not ready, therefore exit with success.
                update_job({
                    'status': JobStatus.FINISHED,
                    'output': json.dumps({'output': 'Successful', 'errors': ''})
                })
                return

            # Normalizes & Shuffles Training Data:
            self.td_preprocess()

            # Create New Model
            self.create_new_model()

            # Train the new model
            self.train_model()

            # Model Selection
            self.model_selection()

            # Identify the best model
            self.identify_best_weights()

            # Post new model
            self.post_model()

            # Context Update
            self.update_context()

            # Update job status to complete
            update_job({
                'status': JobStatus.FINISHED,
                'output': json.dumps({'output': 'Successful', 'errors': ''})
            })

        # Make exception case for error handling
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            log(LogLevel.ERROR, 'Some error in {} ...'.format(
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
    def get_old_and_new_td(self):
        pass

    @abstractmethod
    def validate_td_size(self, update_job):
        pass


    @abstractmethod
    def td_preprocess(self):
        pass
    @abstractmethod
    def create_new_model(self):
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def model_selection(self):
        pass

    @abstractmethod
    def identify_best_weights(self):
        pass

    @abstractmethod
    def post_model(self):
        pass

    @abstractmethod
    def update_context(self):
        pass