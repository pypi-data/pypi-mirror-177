# -*- coding: utf-8 -*-
# Copyright 2022 Valiot. | All Rights Reserved


__author__ = ["alejandro.pasos@valiot.io"]

from datetime import datetime

from ValiotWorker.worker import DEFAULT_EVENT_CONFIG

from factoryos_lib.filters import MovingAverage
from factoryos_lib.filters import ExponentialMovingAverage


def ma_filter_executor(job, log, update_job, get_job_status, context, update_context, **kwargs):
    f = MovingAverage()
    f.execute(job, log, update_job, get_job_status, context, update_context, **kwargs)


def ema_filter_executor(job, log, update_job, get_job_status, context, update_context, **kwargs):
    f = ExponentialMovingAverage()
    f.execute(job, log, update_job, get_job_status, context, update_context, **kwargs)


job_functions = {
    #    "Snapshot": execute_snapshot,
    #    "NNModel": model_executor,
    #    "GateKeeperTimer": execute_alerts,
    #    "FuzzyModel": execute_fuzzy_model,
    "MovingAverage": ma_filter_executor,
    "ExponentialMovingAverage": ema_filter_executor

}


def execute_jobs(worker, jobs):
    for job in jobs:
        parameters = {
            'name': job["parameters"]["name"],
            'alias': job["parameters"]["alias"],
            'description': job["parameters"]["description"],
            'schedule': job["parameters"]["schedule"],
            'type': job["parameters"]["queueType"].value,
            'query': '',
            'lockRequired': job["parameters"]["lockRequired"],
            'function': job_functions[job["model"]],
            "last_run_at": datetime.now(),
            "enabled": True,
            "input": job["input"]

        }
        worker.queues[job["parameters"]["name"]] = parameters
        worker.eventQueues[job["parameters"]["name"]] = {
            "name": job["parameters"]["name"],
            "function": job_functions[job["model"]],
            "mailbox": [],
            "config": {**DEFAULT_EVENT_CONFIG, **DEFAULT_EVENT_CONFIG},
            "start_time": None  # Time to track, if elapsed and mailbox not empty, trigger event
        }
