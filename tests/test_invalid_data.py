#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from job_queue_exporter.slurm_parser import parse_output

# function to test invalid squeue text files
def test_invalid_data():
    counter = 0

    dir_path = os.path.dirname(os.path.realpath(__file__))
    datefile = os.path.join(dir_path, 'data', 'slurm-out-invalid.txt')

    with open(datafile) as my_file:
        invalid_output_array = my_file.readlines()
        invalid_dict = parse_output(invalid_output_array)
        print(invalid_dict)

        for key in invalid_dict:
            squeue_jobs = invalid_dict[key]
            for key2 in squeue_jobs:
                counter += int(squeue_jobs[key2])
        assert(counter == 25)
