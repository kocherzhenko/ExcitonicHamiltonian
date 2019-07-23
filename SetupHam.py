#!/usr/bin/python

#========================================================================================
# Script for setting up Hamiltonian from excitation energies and couplings
# (c) Aleksey A. Kocherzhenko, February 18, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():
#========================================================================================

    SIZE = int(sys.argv[3])

    HamMatrix = [[]]
    number = 1
    # Read in excited state info from file
    for line in open(sys.argv[2]):
        info = line.split()
        if int(info[0]) != number:
           HamMatrix.append([])
           number = int(info[0])
        HamMatrix[-1].append(float(info[2]))

    i = 0   
    for line in open(sys.argv[1]):
#        info = line.split()
#        i = int(info[0])-1
        HamMatrix[i].append(float(line))
        i += 1

#    for el in HamMatrix:
#        print len(el)
#        print el

    for i in range(SIZE):
       for j in range(SIZE):
           if j <= i:
              print '{:>8} {:>8} {:>20.10f}'.format(i+1, j+1, float(HamMatrix[i][j]))
           else:
              print '{:>8} {:>8} {:>20.10f}'.format(i+1, j+1, float(HamMatrix[j][i]))
       print

main()
 
