#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from job_queue_exporter.slurm_parser import parse_output

# function to test valid squeue text files
def test_summary():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    datafile = os.path.join(dir_path, 'data', 'slurm-out-valid.txt')

    # we know before hand this are the right results
    allegro = {
        'PENDING': 2,
        'RUNNING': 1,
        'COMPLETING': 5,
        'COMPLETED': 1,
    }
    lofar = {
        'PENDING': 1,
        'RUNNING': 1,
        'SUSPENDED': 1,
        'COMPLETING': 1,
        'COMPLETED': 1,
    }
    projectmine = {
        'PENDING': 1,
        'COMPLETING': 3,
        'COMPLETED': 1,
    }
    sksp = {
        'PENDING': 1,
        'RUNNING': 2,
        'COMPLETED': 2,
    }
    spexone = {
        'RUNNING': 1,
    }

    with open(datafile, 'r') as df:
        lines = df.readlines()
        result = parse_output(lines)

        assert(result['allegro'] == allegro)
        assert(result['lofar'] == lofar)
        assert(result['projectmine'] == projectmine)
        assert(result['sksp'] == sksp)
        assert(result['spexone'] == spexone)
