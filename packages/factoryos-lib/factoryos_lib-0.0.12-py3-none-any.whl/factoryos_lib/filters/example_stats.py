from ValiotWorker import QueueType, ValiotWorker

from factoryos_lib.filters._stats import Stats

vw = ValiotWorker()

@vw.job(name='TEST_DATA_STATS',
        alias='TEST_DATA_STATS',
        description="t",
        queueType=QueueType.ON_DEMAND,
        schedule="*/60 * * * *",
        enabled=True,
        lockRequired=True
        )
def stats_executor(job, log, update_job, get_job_status, context, update_context, **kwargs):
    f = Stats()
    kwargs = {"input": {
        "variable": "TEST_DATA"
    }}
    f.execute(job, log, update_job, get_job_status, context, update_context, **kwargs)
