#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from slurm_parser import parse_output


# function to test invalid squeue text files
def test_invalid_data():
    counter = 0

    with open('data/slurm-out-invalid.txt') as my_file:
        invalid_output_array = my_file.readlines()
        invalid_dict = parse_output(invalid_output_array, dict())
        print(invalid_dict)

        for key in invalid_dict:
            squeue_jobs = invalid_dict[key]
            for key2 in squeue_jobs:
                counter += int(squeue_jobs[key2])
        assert(counter == 25)
