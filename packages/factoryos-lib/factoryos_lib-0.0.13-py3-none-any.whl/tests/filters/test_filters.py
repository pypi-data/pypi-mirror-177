from ValiotWorker import QueueType

from factoryos_lib.execution import execute_jobs
from factoryos_lib.execution import get_worker, create_job, get_job_status

jobs = [
    {
        "model": "MovingAverage",
        "parameters": {
            "name": 'TEST_DATA_MA_FILTER',
            "alias": '',
            "description": "Description",
            "queueType": QueueType.FREQUENCY,
            "schedule": "*/60 * * * *",
            "enabled": True,
            "lockRequired": True

        },
        "input": {
            "variable": "TEST_DATA",
            "window": 10,
            "block_size": 50,
            "restart": False
        }
    }
]

worker, gql = get_worker()
execute_jobs(worker, jobs)
id_job = create_job()


def test_create_job():
    assert id_job is not None


def test_finish_job():
    worker.eventLoop(interval=2)
    i = 1
    status = get_job_status("TEST_DATA_MA_FILTER", id_job)
    while status == "WAITING":
        worker.eventLoop(interval=2)
        status = get_job_status("TEST_DATA_MA_FILTER", id_job)
        i = i + 1
        if i > 5:
            assert False
    assert True


def test_close_job():
    worker.unlockFinishedJobs(force=True)
    worker.gql.close()
    assert True


def test_results_job():
    assert True
