#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prometheus_client import start_http_server, Gauge
from job_queue_exporter.slurm_parser import parse_output
import time
import subprocess
import argparse
import sys

# shell command to get squeue information
CMD = 'squeue_dummy'
# prometheus client exporter settings
# update squeue info every 30 seconds
UPDATE_PERIOD = 5
# create prometheus gauge
SQUEUE_JOBS = Gauge('squeue_jobs',
                    'hold info on current squeue slurm jobs',
                    ['job_type', 'slurm_group'])


def main():
    my_parser = argparse.ArgumentParser(description='Scheduler job queue information command')
    my_parser.add_argument('-c',
                           '--command',
                           nargs='?',
                           const=CMD,
                           type=str,
                           default=CMD,
                           help='the command to get job queue information')

    args = my_parser.parse_args()
    command = vars(args)['command'].split()

    # start up the server to expose the metrics
    try:
        start_http_server(8000)
    except Exception:
        print('Port 8000 already in use.\nClose port and run again.')
        sys.exit()

    while True:
        output_array = []

        # call squeue.py to retrieve slurm squeue sample output
        # this command will be later replaced by slurm.squeue command
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
        except Exception:
            print('Scheduler job queue command is not compatible.\n\
                Fix using --command flag and run again.')
            sys.exit()

        # read stdout line-by-line & convert from bytes to str
        while True:
            output = process.stdout.readline().decode('utf-8')

            # while stdout is not empty
            if not output:
                break

            output_array.append(output)

        # call function that will parse stdout output
        dictionary = parse_output(output_array)

        # loop through data
        # create gauge objects containing integer value associated with
        # job_type & slurm_group
        for key in dictionary:
            squeue_jobs = dictionary[key]
            for key2 in squeue_jobs:
                SQUEUE_JOBS.labels(job_type=key2,
                                   slurm_group=key).set(squeue_jobs[key2])

        # generate squeue info every UPDATE_PERIOD seconds
        time.sleep(UPDATE_PERIOD)
