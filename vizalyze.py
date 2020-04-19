#!/usr/bin/python3

"""Visible voice bill parser"""

import csv
import warnings
import collections
import argparse


def parse_csv(filename):
    """Read CSV file info a list"""
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        allcalls = list(csvreader)
    return allcalls


def tofromsplit(raw, selfnum):
    """Tag call records with to or from"""
    outarray = []
    for call in raw:
        if (call['Calling_Party_Number'] == selfnum and
                call['Called_Party_Number'] != selfnum):
            call['other'] = call['Called_Party_Number']
            call['outbound'] = True
            outarray.append(call)
        elif (call['Calling_Party_Number'] != selfnum and
              call['Called_Party_Number'] == selfnum):
            call['other'] = call['Calling_Party_Number']
            call['outbound'] = False
            outarray.append(call)
        else:
            warnings.warn('Cannot parse record {}'.format(call))
    return outarray


def tallycalls(parsed):
    """Count # of calls in and out"""
    incount = collections.defaultdict(int)
    outcount = collections.defaultdict(int)
    for call in parsed:
        if call['outbound']:
            outcount[call['other']] += 1
        else:
            incount[call['other']] += 1
    return outcount, incount


def printsorted(mydict):
    """Print a dictionary sorted by its items"""
    for key, value in sorted(mydict.items(), key=lambda item: item[1]):
        print("%s: %s" % (key, value))


def doit(filename, selfnum):
    """Read file and print tallys"""
    outcount, incount = tallycalls(tofromsplit(parse_csv(filename), selfnum))
    print('OUT')
    printsorted(outcount)
    print()
    print('IN')
    printsorted(incount)
    print()


def cli():
    """CLI"""
    parser = argparse.ArgumentParser(description='Process call records.')
    parser.add_argument('filename', help='CSV file')
    parser.add_argument('MDN', help='Self MDN')
    args = parser.parse_args()
    doit(args.filename, args.MDN)


if __name__ == '__main__':
    cli()
