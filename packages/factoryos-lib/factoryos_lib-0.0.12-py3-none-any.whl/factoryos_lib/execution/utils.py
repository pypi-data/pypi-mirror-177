import os
from multiprocessing import SimpleQueue

from ValiotWorker import ValiotWorker, PollingMode, JobConfigMode
from ValiotWorker.Logging import LogStyle, LogLevel
import multiprocessing as mp

from factoryos_lib.execution.config import setup_gql

gql = setup_gql()
worker = ValiotWorker()
worker.setClient(gql)
worker.setWorker(os.environ.get('WORKER'))
worker.setPollingMode(PollingMode.QUERY)
worker.setLoggingStyle(LogStyle.PREFIX_FIRST_LINE)


def get_worker():
    worker.context = mp.get_context('fork')
    worker.getWorker()
    # worker.startLoggingLoop()
    worker.log = worker.getProcessLoggerFunction()
    for queue_name, _ in worker.queues.items():
        worker.logQueues[queue_name] = SimpleQueue()
    worker.abortStaleJobs()
    if worker.jobConfigMode == JobConfigMode.SYNC:
        worker.updateAvailableQueues()
        worker.updateWorkerQueues()
    else:
        worker.log(
            LogLevel.INFO, 'No config sync performed. If required, set jobConfigMode to SYNC')
    if worker.pollingMode == PollingMode.SUBSCRIPTION:
        worker.registerJobCreatedSubscription()
    worker.registerEventJobs()
    worker.registerJobUpdatesListener()
    if worker.useRedis:
        worker.redis.setLog(worker.log)
        worker.redis.initializeRedis()
    worker.registerContinuousJobs()
    return worker, gql


CREATE_JOB = '''
mutation create_job {
  createJob(
    workerCode: "LOCALHOST-Jorge"
    queueName: "TEST_DATA_MA_FILTER"
    jobStatus: WAITING
  ) {
    messages {
      message
      code
      field
    }
    successful
    result {
      id
    }
  }
}
'''


def create_job():
    data, errors = gql.mutate(CREATE_JOB)
    print(data)
    print(errors)
    return data["result"]["id"]


GET_JOB_STATUS = '''
query($Queue:String, $IdString:ID) {
  jobs(
    limit: 1
    orderBy: {desc: INSERTED_AT}
    filter:{queueName:$Queue
            id:$IdString}
  ){
    id
    queue {
      id
      name
    }
    jobStatus
    input
    context
  }
}
'''


def get_job_status(queue, id_string):
    data, errors = gql.query_one(GET_JOB_STATUS, variables={"Queue": queue, "IdString": id_string})
    print(data)
    print(errors)
    return data["jobStatus"]
