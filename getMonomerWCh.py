#!/usr/bin/python

#========================================================================================
# Script for setting up monomer calculations with charges
# (c) Aleksey A. Kocherzhenko, July 26, 2016
#========================================================================================
#   Imports
import sys
import math
import os
#========================================================================================

def main():
#========================================================================================

    TOTAL_MOLECULES = int(sys.argv[1])

    for i in range(TOTAL_MOLECULES):
      f_out = open('monomer_{:04d}_wCh.com'.format(i+1), 'w')
      f_in = open('monomerOptions.txt', 'r')
      f_out.write('%chk=monomer_{:04d}_wCh.chk\n'.format(i+1))
      for line in f_in:
        f_out.write(line)
      f_in.close()
      f_in = open('monomer_{:04d}.xyz'.format(i+1), 'r')
      for line in f_in:
        if len(line.split()) == 4:
          f_out.write(line)
      f_out.write('\n')
      f_in.close()
      for j in range(TOTAL_MOLECULES):
        if j !=i:
          f_in = open('monomer_{:04d}.chg'.format(j+1), 'r')
          for line in f_in:
             f_out.write(line)
          f_in.close()
      f_out.write('\n')
      f_out.close()
         
    return 0
            
main()
 
