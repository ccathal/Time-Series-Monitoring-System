#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Slurm Squeue Parser

Parses squeue string array data and orders the data into nested map.

This file can be imported as a module and contains the following 
functions:
    * parse_output: returns a nested map containing necessary squeue info
"""

def parse_output(output_array):
    """Parses squeue string array data and creats a nested map
    containing necessary squeue data.

    Parameters
    ----------
    output_array : array
        Array of str containing squeue data


    Returns
    -------
    dict{dict{}}
        nested dictionary ict{project_name: dict{job_type: integer}} 
    """

    squeue_info = {}

    for output in output_array:
        # split line into array based on commas
        line_array = output.strip().split(',')

        # make sure line is valid
        try:
            if(len(line_array) == 12):
                project = line_array[2]
                state = line_array[9]
                try:
                    # if state is only 1 word
                    if(len(state) > 0 and ' ' not in state):
                        # 1. setdefault will return the squeue[project] value and,
                        # if necesary it will initialize the value with an empty dict
                        # 2. setdefault will initialise job state with value 0,
                        # if job state not already present
                        # 3. increment job state value
                        values = squeue_info.setdefault(project, {})
                        values.setdefault(state, 0)
                        values[state] += 1
                except:
                    print('Invalid job type. Ignoring stdout squeue output line: {}'.format(ouput))
        except:
            print('Squeue output line does not contain all 12 parameters. Ignoring stdout squeue output line: {}'.format(output))
    return squeue_info
