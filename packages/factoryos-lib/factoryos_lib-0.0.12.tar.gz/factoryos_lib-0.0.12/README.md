# Valiot Data Science Library

This is a repository of data science algorithms using Valiot Worker jobs as base

# Current list of algorithms

1. MovingAverage: Uses the average of the last n elements
2. Stats: Calculate the standard deviation and variance anc store in a variable

# Installation
```
pip install factoryos_lib
```

# Getting started

Create a job and call the execute function

```
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
```
