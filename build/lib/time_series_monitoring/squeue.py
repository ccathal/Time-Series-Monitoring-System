#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import random

# squeue --all -h --format=%A,%j,%a,%g,%u,%P,%v,%D,%C,%T,%V,%M
#
# 49351,tmpDCNGHO,lofarvwf,lofarvwf-fsweijen,lofarvwf-fsweijen,normal,(null),1,5,RUNNING,2020-07-16T20:28:50,1:58:41
# 49358,tmpDCNGHO,lofarvwf,lofarvwf-fsweijen,lofarvwf-fsweijen,normal,(null),1,5,RUNNING,2020-07-16T20:28:50,1:58:41
#
# columns = ['jobid', 'stepname', 'account',
#            'groupname', 'username',
#            'partition', 'reservation',
#            'numnodes', 'numcpus', 'state',
#            'submittime', 'timeused']


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-s', '--seed',
                        action='store',
                        dest='seed',
                        type=int,
                        default=None,
                        help='pseudorandom seed')
    parser.add_argument('-n',
                        action='store',
                        dest='nlines',
                        type=int,
                        default=None,
                        help='number of lines to generate')

    # we will ignore not recognized params
    args, unknown = parser.parse_known_args()
    if args.seed is not None:
        random.seed(args.seed)

    if args.nlines is None:
        nlines = random.randint(0, 100)
    else:
        nlines = args.nlines

    accounts = ['lofar', 'tropomi', 'sksp', 'spexone', 'allegro', 'projectmine']
    # groupname == username
    user_suffix = ['user001', 'user002', 'user003', 'user004', 'user005']
    states = ['PENDING', 'RUNNING', 'SUSPENDED', 'COMPLETING', 'COMPLETED']
    partitions = ['normal']
    reservations = ['(null)']
    max_nodes = 4
    max_cpus = 4

    offset = random.randint(0, 10000)

    lines = []
    for i in range(nlines):
        words = []
        # jobid
        jobid = i + offset
        words.append(str(jobid))
        # stepname
        words.append('stepname{}'.format(jobid))
        # account
        words.append(random.choice(accounts))
        # groupname (it happens to be the username)
        username = '{}-{}'.format(random.choice(accounts),
                                  random.choice(user_suffix))
        words.append(username)
        # adding again to place it in the position of the username
        words.append(username)
        # partition
        words.append(random.choice(partitions))
        # reservation
        words.append(random.choice(reservations))
        # numnodes
        words.append(str(random.randint(1, max_nodes)))
        # ncpus
        words.append(str(random.randint(1, max_cpus)))
        # state
        words.append(random.choice(states))
        # submit time
        consumed = random.randint(30, 300)
        submit = datetime.datetime.now() - datetime.timedelta(minutes=consumed)
        words.append(submit.strftime('%y-%m-%dT%H:%M:%S'))
        # timeused
        words.append(str(consumed))

        # putting line together
        lines.append(','.join(words))

    # print to stdout
    print('\n'.join(lines))


if __name__ == "__main__":
    main()
