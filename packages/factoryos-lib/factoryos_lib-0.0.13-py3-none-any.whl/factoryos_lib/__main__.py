import os

from ValiotWorker import ValiotWorker, PollingMode, JobConfigMode
from ValiotWorker.Logging import LogStyle

from factoryos_lib.execution.config import setup_gql

# Hide TensorFLow compilation warnings (CUDA, NVIDA etc.)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

gql = setup_gql()
worker = ValiotWorker()
worker.setClient(gql)
worker.setWorker(os.environ.get('WORKER'))
worker.setPollingMode(PollingMode.QUERY)
worker.setLoggingStyle(LogStyle.PREFIX_FIRST_LINE)
worker.setJobConfigMode(JobConfigMode.SYNC)

# Alternative, run jobs without decorator
#execute_jobs(worker, job_list.jobs)


def main():
    worker.run(interval=2)


if __name__ == "__main__":
    main()
