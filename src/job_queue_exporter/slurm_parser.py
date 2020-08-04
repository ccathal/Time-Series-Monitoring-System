#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_output(output_array):
    squeue_info = {}
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

    for output in output_array:

        # split line into array based on commas
        line_array = output.strip().split(',')

        # make sure line is valid
        try:
            if(len(line_array) == 12):
                project = line_array[2]
                state = line_array[9]
                try:
                    if(state in default_values):
                        # setdefault will return the squeue[project] value and, if necesary
                        # it will initialize the value with a copy of "default_values" dict
                        # It is important to make a COPY of default_values
                        values = squeue_info.setdefault(project, dict(default_values))
                        values[state] += 1
                except:
                    print('Invalid job type. Ignoring stdout squeue output line: {}'.format(ouput))
        except:
            print('Squeue output line does not contain all 12 parameters. Ignoring stdout squeue output line: {}'.format(output))

    return squeue_info
