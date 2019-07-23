#!/usr/bin/python

#========================================================================================
# Script for switching signs in configuration coefficients
# (c) Aleksey A. Kocherzhenko, April 1, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():
#========================================================================================
#   Input parameters

    NUM_STATES = int(sys.argv[2])-1

#========================================================================================
    PI = 3.14159265358

#    inverted = open('inverted.log', 'w');

    flag = False
    line_countdown = -1
    counting = 0
    # Read in Gaussian .log file
    for line in open(sys.argv[1]):
       if 'transition electric' in line:
          line_countdown = 2
       if 'Dipole' in line:
          line_countdown = 1
       if line_countdown > 0:
          line_countdown -= 1
       elif line_countdown == 0:
          elements = line.split()
          if len(elements) == 6:
             tx = float(elements[1])
             ty = float(elements[2])
             tz = float(elements[3])
#             print tx, ty, tz
          elif len(elements) == 8:
             gx = float(elements[1])
             gy = float(elements[3])
             gz = float(elements[5])
#             print gx, gy, gz
          line_countdown -= 1

    angle = math.acos((tx*gx+ty*gy+tz*gz)/math.sqrt(tx*tx+ty*ty+tz*tz)/math.sqrt(gx*gx+gy*gy+gz*gz))
#    print angle

    if angle < PI/2.0:
       exit
    else:
       for line in open(sys.argv[1]):
          if flag == False:
             if 'transition electric' in line:
               line_countdown = 3
             if line_countdown > 0:
               line_countdown -= 1
             if line_countdown == 0:
               tdm = line.split()
               X = -float(tdm[1])
               Y = -float(tdm[2])
               Z = -float(tdm[3])
               print '{:10d} {:14.4f} {:11.4f} {:11.4f} {:11.4f} {:11.4f} \n'.format(int(tdm[0]), X, Y, Z, float(tdm[4]), float(tdm[5])),
               line_countdown -= 1
               counting = NUM_STATES
             else: 
               if counting > 0:
                 tdm = line.split()
                 X = -float(tdm[1])
                 Y = -float(tdm[2])
                 Z = -float(tdm[3])
                 print '{:10d} {:14.4f} {:11.4f} {:11.4f} {:11.4f} {:11.4f} \n'.format(int(tdm[0]), X, Y, Z, float(tdm[4]), float(tdm[5])),
                 counting -= 1 
               else:
                 print line,

          if flag == True:
             if ('>' in line) or ('<' in line):
#                print line,
                elements = line.split()
                print ' ',
                for el in elements[:-1]:
                   print el,
                if elements[-1][0] == '-':
                   print elements[-1][1:]
                else:
                   print '-'+elements[-1]
             else:
                flag = False

          if 'Excited State' in line:
             flag = True
    
    return 0

main()
 
