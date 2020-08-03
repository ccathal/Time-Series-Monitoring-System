#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from slurm_parser import parse_output
from job_queue_exporter.slurm_parser import parse_output
import os

# function to test valid squeue text files
def test_valid_data():
    counter = 0
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    datafile = os.path.join(dir_path, 'data', 'slurm-out-valid.txt')

    with open(datafile) as my_file:
        valid_output_array = my_file.readlines()
        valid_dict = parse_output(valid_output_array)
        print(valid_dict)

        for key in valid_dict:
            squeue_jobs = valid_dict[key]
            for key2 in squeue_jobs:
                counter += int(squeue_jobs[key2])
        assert(counter == 25)
