#!/usr/bin/python

#========================================================================================
# Script for getting the CHelpG charges
# (c) Aleksey A. Kocherzhenko, July 26, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():
#========================================================================================

    NATOMS = int(sys.argv[2])

    flag_coords = False
    coord_list = []
    flag_charges = False
    charge_list = []

    for line in open(sys.argv[1]):

      # Get coordinates or CHelpG charges, otherwise skip line
      if (flag_coords == False) and ('Symbolic' not in line) and (flag_charges == False) and ('ESP charges:' not in line):
        continue
      elif ('Symbolic' in line):
#        print line
        flag_coords = True
        counter = -1
      elif (flag_coords == True):
        counter += 1
        if counter < 1:
          continue
        elif counter > NATOMS:
          flag_coords = False
          continue
        else:
          coords = (line.split())[1:]
          coord_list.append(coords)
#          print coord_list[-1]
      elif ('ESP charges:' in line):
#        print line
        flag_charges = True
        counter = -1
      elif (flag_charges == True):
        counter += 1
        if counter < 1:
          continue
        elif counter > NATOMS:
          break
        else:
          charges = (line.split())[-1]
          charge_list.append(charges)
#          print charge_list[-1]
    
# Write coordinates (x,y,z) and charges to file     
    filename = (sys.argv[1])[:-3] + 'chg'
    file_out = open(filename ,"w")
    for i in range(NATOMS):
      line = ''
      for j in range(3):
        line += coord_list[i][j].rjust(12)
      line += charge_list[i].rjust(12)
#      print line
      file_out.write(line+'\n')
    file_out.close() 
      
   
    return 0
            
main()
 
