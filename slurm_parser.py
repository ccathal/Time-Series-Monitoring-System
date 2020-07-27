#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def parse_output(output_array, squeue_info):
    
    for output in output_array:

        # split line into array based on commas
        line_array = output.strip().split(',')

        # make sure line is valid
        if(len(line_array) == 12):
            # if project_group does not already exist as key in dictionary
            # add project_group as new key to dictionaryset default_values dict as value
            if line_array[2] not in squeue_info:
                default_values = {
                    'PENDING': 0,
                    'RUNNING': 0,
                    'SUSPENDED': 0,
                    'CANCELLED': 0,
                    'COMPLETING': 0,
                    'COMPLETED': 0,
                    'CONFIGURING': 0,
                    'FAILED': 0,
                    'TIME_OUT': 0,
                    'PRE_EMPTED': 0,
                    'NODE_FAIL': 0,
                    }
                squeue_info.setdefault(line_array[2], default_values)

            # increment integer value in squeue_info dict associated with the job type in the current Slurm output line
            squeue_info[line_array[2]][line_array[9]] += 1

    return squeue_info
