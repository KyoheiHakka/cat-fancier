#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import time
from pprint import pprint


def parsearguments():
    parser = argparse.ArgumentParser(description='run cascade training')
    parser.add_argument('positivefilename', help='positive sample file')
    parser.add_argument('negativefilename', help='negative sample file')
    parser.add_argument('-f', '--maxfarate', help='max false alarm rate',
                        type=float, default=0.5)
    parser.add_argument('-d', '--dstdir', help='destination directory',
                        type=str, default='train')
    return parser.parse_args()

def createsamples(positivefile, vecdir='./vec'):
    os.environ['PATH'] = '/bin:/usr/bin:/usr/local/bin'
    if not os.path.isdir(vecdir):
        os.mkdir(vecdir)
    numpos = len(open(positivefile).readlines())
    print('samples: %d' % (numpos,))
    vecfile = vecdir + '/' + positivefile + '.vec'
    cmdline = ['opencv_createsamples', '-info', positivefile,
               '-vec', vecfile, '-num', str(numpos)]
    print(' '.join(cmdline))
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, close_fds=True)
    except OSError as e:
        print(e)
        sys.exit(-1)
    
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line.rstrip())
    ret = p.wait()

    return (vecfile, numpos)

def traincascade(dstdir, vecfile, numpos, negativefilename, maxfarate=0.5):
    if not os.path.isdir(dstdir):
        os.mkdir(dstdir)
    numpos = int(round(numpos*0.85))
    numneg = len(open(negativefilename).readlines())
    cmdline = [
        'opencv_traincascade', '-data', dstdir, '-vec', vecfile,
        '-bg', negativefilename, '-numPos', str(numpos), '-numNeg', str(numneg),
        '-featureType', 'LBP', '-maxFalseAlarmRate', str(maxfarate)
    ]
    print(' '.join(cmdline))
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, close_fds=True)
    except OSError as e:
        print(e)
        sys.exit(-1)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line.rstrip())
    ret = p.wait()

if __name__ == '__main__':
    args = parsearguments()
    positivefilename = args.positivefilename
    negativefilename = args.negativefilename
    maxfarate = args.maxfarate
    dstdir = args.dstdir
    (vecfile, numpos) = createsamples(positivefilename)
    # vecfile = './vec/positive.dat.vec'
    # numpos = len(open(args.positivefilename).readlines())
    traincascade(dstdir, vecfile, numpos, negativefilename, 0.4)
    
    
