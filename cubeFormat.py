#!/usr/bin/python

#========================================================================================
# (c) Aleksey A. Kocherzhenko, January 7, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():

  linenum = 0
  xvector = []
  yvector = []
  zvector = []
  atomnum = 1000000

  xnum = 1
  ynum = 1
  znum = 0

  cube = {}
  
  numpoints = 0

# READ IN CUBE FILE GIVEN AS THE ARGUMENT IN THE COMMAND LINE
  infile = sys.argv[1]
  for line in open(infile):
    linenum += 1
    if linenum < 3: continue
    elif linenum == 3:
      elements = line.split()
      atomnum = int(elements[0])    # Total number of atoms in the molecule
      # Get coordinate system origin:
      xorigin = float(elements[1]) 
      yorigin = float(elements[2])
      zorigin = float(elements[3])
    elif linenum < 7:
      elements = line.split()
      if linenum == 4:
        xsize = int(elements[0])    # Number of grid points in the x direction
        for i in range(3): xvector.append(float(elements[i+1]))   # x-axis vector
#        print xsize, xvector
      if linenum == 5:
        ysize = int(elements[0])    # Number of grid points in the y direction
        for i in range(3): yvector.append(float(elements[i+1]))   # y-axis vector
#        print ysize, yvector
      if linenum == 6:
        zsize = int(elements[0])    # Number of grid points in the z direction
        for i in range(3): zvector.append(float(elements[i+1]))   # z-axis vector
#        print zsize, zvector
        # Check that the x-, y-, and z-axis vectors are all perpendicular
        if ( (xvector[0]*yvector[0] + xvector[1]*yvector[1] + xvector[2]*yvector[2] > 1.e-6) or
             (xvector[0]*zvector[0] + xvector[1]*zvector[1] + xvector[2]*zvector[2] > 1.e-6) or
             (yvector[0]*zvector[0] + yvector[1]*zvector[1] + yvector[2]*zvector[2] > 1.e-6) ):
          print "Grid not rectangular"
          break
        # Calculate the length of the unit cell in x, y, and z directions
        else:
          xunit = math.sqrt(xvector[0]**2 + xvector[1]**2 + xvector[2]**2)
          yunit = math.sqrt(yvector[0]**2 + yvector[1]**2 + yvector[2]**2)
          zunit = math.sqrt(zvector[0]**2 + zvector[1]**2 + zvector[2]**2)

    # Calculate the total number of valence electrons
    elif linenum < 7 + atomnum:
      continue

    # Read in density for all grid points
    else:
      elements = line.split()
      for el in elements:
        znum += 1
        if znum > zsize:
          znum = 1
          ynum += 1
          if ynum > ysize:
            ynum = 1
            xnum += 1
        # dict key specifies position of unit volume, value specifies density within unit volume
        cube[(znum-1)+(ynum-1)*zsize+(xnum-1)*ysize*zsize+1] = float(el)
#        print cube[(znum-1)+(ynum-1)*zsize+(xnum-1)*ysize*zsize+1]
        numpoints += 1

# Integrate transition density over all space and correct for the integral not being exactly zero
  posit = 0
  negat = 0
  for key in sorted(cube.keys()):
    if cube[key] <= 0: negat += cube[key]
    if cube[key] > 0: posit += cube[key]
  epsilon = negat+posit

  unitvolume = xunit*yunit*zunit

# Correction used in Brent Krueger's original paper
#  correction = -(negat+posit)/key
#  negat *= unitvolume
#  posit *= unitvolume

# Scaling, as done by Donghyun Lee
  pos_scale = (posit-0.5*epsilon)/posit
  neg_scale = (negat-0.5*epsilon)/negat

  tot = 0
  for key in sorted(cube.keys()):
# Brent Krueger's original method
#    cube[key] += correction
# Donghyun Lee's version
    if cube[key] <= 0: cube[key] *= neg_scale
    if cube[key] > 0: cube[key] *= pos_scale
    tot += cube[key]

# Write cube to file in input format for TDC calculations
  outfile = infile[:len(infile)-4] + ".fcub"
  
  output = open(outfile, 'w')
  output.write('{} \n\n'.format(numpoints)) 
  for key in sorted(cube.keys()): 
    # Reconstruct x, y, and z coordinate of unit volume from key
    xnum = ((key-1) // (ysize*zsize)) + 1
    ynum = (((key-1) - (xnum-1)*ysize*zsize) // zsize) + 1
    znum = ((key-1) - (ynum-1)*zsize - (xnum-1)*ysize*zsize) + 1
    # Get actual coordinate value for volume
    xcoord = xorigin + (xnum-1)*xvector[0] + (ynum-1)*yvector[0] + (znum-1)*zvector[0]
    ycoord = yorigin + (xnum-1)*xvector[1] + (ynum-1)*yvector[1] + (znum-1)*zvector[1]
    zcoord = zorigin + (xnum-1)*xvector[2] + (ynum-1)*yvector[2] + (znum-1)*zvector[2]
    output.write('{:>15} {:>15} {:>15} {:>20}\n'.format(xcoord, ycoord, zcoord, cube[key]*unitvolume))
  output.write('\n')
  output.close()
  
  

################################################################################################## 
# INTEGRATE DENSITY OVER ALL VOLUME AND CALCULATE DIPOLE MOMENT:
# FOR TESTING PURPOSES ONLY
  dipole_x = 0
  dipole_y = 0
  dipole_z = 0
  for key in sorted(cube.keys()):
    # Reconstruct x, y, and z coordinate of unit volume from key
    xnum = ((key-1) // (ysize*zsize)) + 1
    ynum = (((key-1) - (xnum-1)*ysize*zsize) // zsize) + 1
    znum = ((key-1) - (ynum-1)*zsize - (xnum-1)*ysize*zsize) + 1
    # Get actual coordinate value for volume
    xcoord = xorigin + (xnum-1)*xvector[0] + (ynum-1)*yvector[0] + (znum-1)*zvector[0]
    ycoord = yorigin + (xnum-1)*xvector[1] + (ynum-1)*yvector[1] + (znum-1)*zvector[1]
    zcoord = zorigin + (xnum-1)*xvector[2] + (ynum-1)*yvector[2] + (znum-1)*zvector[2]
    # Calculate dipole moment for molecule
    dipole_x += -cube[key]*xcoord
    dipole_y += -cube[key]*ycoord
    dipole_z += -cube[key]*zcoord
  
  dipole_x *= unitvolume
  dipole_y *= unitvolume
  dipole_z *= unitvolume

  print "Dipole vector: ", dipole_x, dipole_y, dipole_z
  
main()

