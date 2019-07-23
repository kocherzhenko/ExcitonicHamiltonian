#!/usr/bin/python

#========================================================================================
# Script for getting the transition dipole moments
# (c) Aleksey A. Kocherzhenko, April 21, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():
#========================================================================================

    # Read in excited state info from file
    flag = 0
    namelist = sys.argv[1].split('_')
    setsize = namelist[1]
    setnum = namelist[2]
    monomer = namelist[3]
    for line in open(sys.argv[1]):
        info = line.split()
        if "electric" in info:
          flag += 1
        elif flag == 1:
          flag += 1
        elif flag == 2:
          X = info[1]
          Y = info[2]
          Z = info[3]
#          print '{:>8} {:>20} {:>20} {:>20}'.format(monomer, X, Y, Z)
          print setsize, setnum, monomer, X, Y, Z
          return 0
            
main()
 
