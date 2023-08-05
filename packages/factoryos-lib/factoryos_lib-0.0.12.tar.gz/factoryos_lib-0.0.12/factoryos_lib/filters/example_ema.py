from ValiotWorker import QueueType, ValiotWorker

from factoryos_lib.filters import ExponentialMovingAverage

vw = ValiotWorker()


@vw.job(name='Premolienda_Humedad_Silo6_EMA_FILTER',
        alias='Premolienda_Humedad_Silo6_EMA_FILTER',
        description="t",
        queueType=QueueType.ON_DEMAND,
        schedule="*/60 * * * *",
        enabled=True,
        lockRequired=True
        )
def ema_filter_executor(job, log, update_job, get_job_status, context, update_context, **kwargs):
    f = ExponentialMovingAverage()
    kwargs = {"input": {
        "variable": "Premolienda_Humedad_Silo6",
        "window": 20,
        "block_size": 9500,
        "restart": True
    }}
    f.execute(job, log, update_job, get_job_status, context, update_context, **kwargs)
