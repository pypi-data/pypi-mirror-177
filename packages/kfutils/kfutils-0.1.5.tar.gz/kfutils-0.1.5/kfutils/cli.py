#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals, division, print_function

import os
import sys
import logging
import textwrap
import argparse
import glob
import numpy as np
import pkg_resources
from kfutils.funcs import *


__all__ = []
version= pkg_resources.require('kfutils')[0].version

class CustomParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write('\033[91mError: %s\n\033[0m' % message)
        self.print_help()
        sys.exit(2)


def listOfInts(val):
    try:
        val = int(val)
        if val < 0:
            raise ValueError
    except:
        raise argparse.ArgumentTypeError("Only list of positive are allowed")
    return val


def createParser():
    #main parser
    parser = CustomParser(prog="kutils",
                          formatter_class=argparse.RawTextHelpFormatter,
                          description="A tool for common data file operation.",
                          epilog="Version: {}\nCreated by Koushik Naskar (koushik.naskar9@gmail.com)".format(version)
                          )

    #adding options for numerical jobs
    parser.add_argument('-i', type=str, help="Input file name. \nIf no operations are given it will show the stats about the file.", metavar="FILE", required=True)
    parser.add_argument('-o', type=str, help="Output file name", metavar="FILE")
    parser.add_argument('-c', help="index(s) of grid columns. 2 columns for 2D file.", nargs='+', metavar='COLS', type=listOfInts)
    parser.add_argument('-rd', help="index of columns to convert to degree from radian",
                        nargs='+', metavar='COLS',type=listOfInts)
    parser.add_argument('-dr', help="index of columns to convert to radian to degree",
                        nargs='+', metavar='COLS', type=listOfInts)
    parser.add_argument('-dc', help="index of columns to drop", nargs='+', metavar='COLS', type=listOfInts)
    parser.add_argument('-int', help="Interpolate to new number of grid. Can be 1D or 2D.", nargs='+', metavar='COLS', type=listOfInts)
    return parser.parse_args()


def commandGiven(args):
    # check any of these command is given or not
    for elem in ['c','rd','dr','dc']:
        if getattr(args,elem):
            return True
    return False


def main():
    args = createParser()
    inpFile = args.i


    if not commandGiven(args):  
        # no other operations are specified so just show stats
        showStats(args.i)
        return


    cols = args.c
    # read file
    data = np.loadtxt(inpFile)


    if (args.dc):
        print("NOTE: Delete columns will take precedence over other operations.")
        data = np.delete(data, args.dc, axis=1)


    # rad to deg
    if (args.rd):
        data[:, args.rd] = np.rad2deg(data[:, args.rd])
    # deg to rad
    if (args.dr):
        data[:, args.dr] = np.deg2rad(data[:, args.dr])
    # delete columns


    if (args.int):
        assert len(cols)==len(args.int), "Invalid number of columns for interpolation"
        if len(cols)==1:
            data = lineGridInt(data, cols[0], args.int[0])
        elif len(cols)==2:
            data = rectGridInt(data, *cols, *args.int)



    # now write file
    outFile = args.o
    if not outFile:
        outFile = "{}_out{}".format(*os.path.splitext(inpFile))

    if len(cols) == 1:  #1D file
        write1DFile(outFile, data)
    else:
        writeFile(outFile, data, cols[0])



    print(f"File saved as {outFile}")


if __name__ == "__main__":
    main()