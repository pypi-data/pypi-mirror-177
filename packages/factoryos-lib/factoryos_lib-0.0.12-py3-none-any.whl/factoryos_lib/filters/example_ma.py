from ValiotWorker import QueueType, ValiotWorker

from factoryos_lib.filters import MovingAverage

vw = ValiotWorker()


@vw.job(name='TEST_DATA_MA_FILTER',
        alias='TEST_DATA_MA_FILTER',
        description="t",
        queueType=QueueType.ON_DEMAND,
        schedule="*/60 * * * *",
        enabled=True,
        lockRequired=True
        )
def ma_filter_executor(job, log, update_job, get_job_status, context, update_context, **kwargs):
    f = MovingAverage()
    kwargs = {"input": {
        "variable": "TEST_DATA",
        "window": 10,
        "block_size": 150,
        "restart": True
    }}
    f.execute(job, log, update_job, get_job_status, context, update_context, **kwargs)
