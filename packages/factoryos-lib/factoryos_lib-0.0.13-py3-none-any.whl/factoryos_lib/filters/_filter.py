# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved

__author__ = ["FactoryOS Team"]

import json
import sys
import pydash as __
from abc import abstractmethod
from ValiotWorker import JobStatus
from ValiotWorker.Logging import LogLevel

from factoryos_lib.base import Component
from . import queries as q
from factoryos_lib.base import mutations as m


class NotEnoughDataException(Exception):
    pass


class Filter(Component):
    """ Filter
           Overview:
           - Abstract class to define a reusable filter
           -The filter retrieves information from a Variable and store the filtered
            data in a different variable

           Parameters
           ----------
           log_callback : name of the model
           job_name : json structure for the model
           context : dictionary with persistent data to retrieve between executions
           update_context : function to update context

           X : Input
           Y:  Filtered data (output)
           X_name : Name of the input variable
           Y_name:  Name of the output variable
           Y_id: output data ids
           window: Window for the filter
           block_size: Size of the block of data to retrieve in this execution

           """

    def __init__(self):
        self.restart = None
        self.log_callback = None
        self.job_name = None
        self.context = None
        self.update_context = None

        self.X = None
        self.X_name = None
        self.Y = None
        self.Y_name = None
        self.Y_id = None
        self.window = None
        self.block_size = None

    def initialize(self, job, log, update_job, context, update_context):
        self.log_callback = log
        self.job_name = job["queue"]["name"]
        self.Y_name = self.job_name
        self.context = context
        self.update_context = update_context

    def execute(self, job, log, update_job, get_job_status, context, update_context, **kwargs):
        log(LogLevel.DEBUG, '{} is running ...'.format(job["queue"]["name"]))
        update_job({'status': JobStatus.RUNNING, 'progress': 0})

        try:
            self.initialize(job, log, __, context, update_context)
            self.set_inputs(kwargs)
            self.get_data()
            self.apply_filter()
            self.post_data()
            log(LogLevel.INFO, 'Finished successfully job {}...'.format(job["queue"]["name"]))

            update_job({
                'status': JobStatus.FINISHED,
                'output': json.dumps({'output': 'Successful', 'errors': ''})
            })

        except NotEnoughDataException:
            log(LogLevel.INFO, 'Not enough data yet to run filter {}... finished job'.format(job["queue"]["name"]))
            update_job({
                'status': JobStatus.FINISHED,
                'output': json.dumps({'output': 'Successful', 'errors': ''})})
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            log(LogLevel.ERROR, 'Some error with {}...'.format(job["queue"]["name"]))
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

    def check_filter_variable(self):
        if not q.exist_variable(self.Y_name, self):
            self.log_callback(LogLevel.DEBUG,
                              "Variable {} does not exist, creating a new variable.".format(self.Y_name))
            m.create_variable(self.Y_name, self)

    def check_data_count(self):
        count_variable_in = q.get_variable_count(self.X_name, self)
        count_variable_out = q.get_variable_count(self.Y_name, self)

        if count_variable_in > count_variable_out:

            data_to_insert = count_variable_in - count_variable_out
            self.log_callback(LogLevel.DEBUG, f"New data found inserting {data_to_insert} datum in {self.Y_name} ")
            for i in range(data_to_insert):
                m.create_datum(self.Y_name, 0, self)

            self.log_callback(LogLevel.DEBUG, f"Completed inserting {data_to_insert} datum in {self.Y_name} ")

    @abstractmethod
    def set_inputs(self, kwargs):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def post_data(self):
        pass

    @abstractmethod
    def apply_filter(self):
        pass
