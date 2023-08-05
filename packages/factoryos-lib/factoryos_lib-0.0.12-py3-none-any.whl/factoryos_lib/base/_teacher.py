# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["FactoryOS Team"]

import sys
from abc import abstractmethod
import json

from ValiotWorker import JobStatus
from ValiotWorker.Logging import LogLevel
from factoryos_lib.base._component import Component


class Teacher(Component):
    """ Teacher
               Overview:
               - Abstract class to define a reusable teacher
               Parameters
               ----------
               teacher_parameters : ist of parameters
               controller_model_name :  name of the controller
               controller_model_json : json structure for the model
               last_td : last train data

           """
    def __init__(self):
        super.__init__(self)
        self.teacher_parameters = None
        self.controller_model_name = None
        self.controller_model_json = None
        self.last_td = None

    @abstractmethod
    def initialize(self,job, log):
        pass

    def execute(self, job, log, update_job):
        log(LogLevel.DEBUG, '{} is running ...'.format(job["queue"]["name"]))
        update_job({'status': JobStatus.RUNNING, 'progress': 0})

        try:
            # Initialize teacher Object.
            self.initialize(job, log)

            # Gets the model from Valiot DB.
            self.get_model_from_db()

            # Sets teacher attributes with Model Info.
            self.set_model_parameters()

            # Get last training data.
            self.get_last_td()

            # Get current state.
            self.get_td_values()

            # Checks if the item is the same as the previous one.
            self.check_td_repeated()

            # Check the range of every input.
            self.check_td_in_range()

            # If the TD is unique and in the desired range, post it.
            self.post_new_td()

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
    def get_model_from_db(self):
        pass

    @abstractmethod
    def set_model_parameters(self):
        pass

    @abstractmethod
    def get_last_td(self):
        pass

    @abstractmethod
    def get_td_values(self):
        pass

    @abstractmethod
    def check_td_repeated(self):
        pass

    @abstractmethod
    def check_td_in_range(self):
        pass

    @abstractmethod
    def post_new_td(self):
        pass


