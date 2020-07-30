#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slurm_parser import parse_output


# function to test valid squeue text files
def test_summary():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    datafile = os.path.join(dir_path, 'data', 'slurm-out-valid.txt')

    # we know before hand this are the right results
    allegro = {
        'PENDING': 2,
        'RUNNING': 1,
        'SUSPENDED': 0,
        'CANCELLED': 0,
        'COMPLETING': 5,
        'COMPLETED': 1,
        'CONFIGURING': 0,
        'FAILED': 0,
        'TIME_OUT': 0,
        'PRE_EMPTED': 0,
        'NODE_FAIL': 0
    }
    lofar = {
        'PENDING': 1,
        'RUNNING': 1,
        'SUSPENDED': 1,
        'CANCELLED': 0,
        'COMPLETING': 1,
        'COMPLETED': 1,
        'CONFIGURING': 0,
        'FAILED': 0,
        'TIME_OUT': 0,
        'PRE_EMPTED': 0,
        'NODE_FAIL': 0
    }
    projectmine = {
        'PENDING': 1,
        'RUNNING': 0,
        'SUSPENDED': 0,
        'CANCELLED': 0,
        'COMPLETING': 3,
        'COMPLETED': 1,
        'CONFIGURING': 0,
        'FAILED': 0,
        'TIME_OUT': 0,
        'PRE_EMPTED': 0,
        'NODE_FAIL': 0
    }
    sksp = {
        'PENDING': 1,
        'RUNNING': 2,
        'SUSPENDED': 0,
        'CANCELLED': 0,
        'COMPLETING': 0,
        'COMPLETED': 2,
        'CONFIGURING': 0,
        'FAILED': 0,
        'TIME_OUT': 0,
        'PRE_EMPTED': 0,
        'NODE_FAIL': 0
    }
    spexone = {
        'PENDING': 0,
        'RUNNING': 1,
        'SUSPENDED': 0,
        'CANCELLED': 0,
        'COMPLETING': 0,
        'COMPLETED': 0,
        'CONFIGURING': 0,
        'FAILED': 0,
        'TIME_OUT': 0,
        'PRE_EMPTED': 0,
        'NODE_FAIL': 0
    }

    with open(datafile, 'r') as df:
        lines = df.readlines()
        result = parse_output(lines)

        assert(result['allegro'] == allegro)
        assert(result['lofar'] == lofar)
        assert(result['projectmine'] == projectmine)
        assert(result['sksp'] == sksp)
        assert(result['spexone'] == spexone)
