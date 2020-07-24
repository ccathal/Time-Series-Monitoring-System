#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import squeue
import json


def main():

    # call squeue.py main method to retrieve slurm squeue sample output
    # this command will be later replaced by slurm.squeue command
    info = squeue.main()

    # write ouput to file
    f = open('parse.txt', 'w')
    f.write(info)
    f.close()

    try:
        # final data structure will be a nested dictonary
        # JLF: you just need var = {} or var = dict() to start a new dict.
        squeue_info = dict()

        # open file data has been previously written to & read line-by-line
        with open('parse.txt', 'r') as fp:
            line = fp.readline()

            # while line still exists in text file
            while line:

                # split line into array
                line_array = line.split(',')

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
                    squeue_info[line_array[2]] = default_values

                # increment integer value in squeue_info dict associated with the job type in the current Slurm output line
                squeue_info[line_array[2]][line_array[9]] += 1

                # read next slurm output line
                line = fp.readline()

            # print final nested dictionary in json format
            print('End of squeue output. Final parsed squeue output:\n')
            print(json.dumps(squeue_info, indent=4))
            return squeue_info

    finally:
        fp.close()


if __name__ == "__main__":
    main()