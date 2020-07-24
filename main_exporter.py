#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prometheus_client import start_http_server, Gauge
import slurm_parser
import time

# prometheus client exporter settings
# update squeue info every 30 seconds
UPDATE_PERIOD = 30
# create prometheus gauge
SQUEUE_JOBS = Gauge('squeue_jobs',
                    'hold info on current squeue slurm jobs',
                    ['job_type', 'slurm_group'])


if __name__ == "__main__":

    # start up the server to expose the metrics
    start_http_server(8000)

    # generate some requests
    while True:
        # parse.py main method generates and parses squeue data into python dict
        dictionary = slurm_parser.main()

        # loop through data
        # create gauge objects containing integer value associated with
        # job_type & slurm_group
        for key in dictionary:
            squeue_jobs = dictionary[key]
            for key2 in squeue_jobs:
                SQUEUE_JOBS.labels(job_type=key2, slurm_group=key).set(squeue_jobs[key2])
        # generate squeue info every UPDATE_PERIOD seconds
        time.sleep(UPDATE_PERIOD)
