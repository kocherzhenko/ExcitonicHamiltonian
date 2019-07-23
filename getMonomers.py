#!/usr/bin/python

#========================================================================================
# Script for generating files with coordinates of individual chromophores
# (c) Aleksey A. Kocherzhenko, January 12, 2016
#========================================================================================
#   Imports
import sys
import math
#========================================================================================

def main():
#========================================================================================
#   Input parameters

    ATOMS_PER_MOLECULE = int(sys.argv[2]) # number of atoms per molecule
    
#========================================================================================

    lead_index = 0
    
    atom_coords = []
    totalatoms = 0
    index = 1

    molecule = []
    moldict = {}

    lead_lines = 0    
    # Read in .mol2 file
    for line in open(sys.argv[1]):
        # Skip lead lines
        if lead_lines == 0 and ('ATOM' not in line):
            continue
        elif 'ATOM' in line:
            lead_lines = 1
        # Read in atomic coordinates
        else:        
            atom_coords = line.split()
            totalatoms += 1
            if atom_coords.pop(0) == '@<TRIPOS>BOND':
                break
            else:
                # Remove unnecessary information  
                atom_coords.pop(-1)
                atom_coords.pop(-2)
                atom_coords.pop(-2)
                # Convert atomic coordinates x,y,z from strings to real numbers
                for i in range(1,4):
                   atom_coords[i] = float(atom_coords[i])
                atom_coords.pop(-1)
 
#                print atom_coords
#                print totalatoms
                molecule.append(atom_coords)
 
                # Finished analyzing one molecule in snapshot, move on to the next
                if totalatoms == ATOMS_PER_MOLECULE:
                   moldict[index] = molecule[:]
                   totalatoms = 0
                   index += 1
                   molecule = []
            
    for key in sorted(moldict.keys()): 
       totalatoms = 0   
       # Write monomer files
       monomer_filename = 'monomer_{:04d}.xyz'.format(key)
       print 'Writing ', monomer_filename, '...'
       monomer_file = open(monomer_filename, 'w')      
       monomer_file.write('{:<8}\n\n'.format(ATOMS_PER_MOLECULE))
       for atom_coords in moldict[key]:
          monomer_file.write('{:<5} {:>15} {:>15} {:>15} \n'.format(*atom_coords))
#       monomer_file.write('\n')
       monomer_file.close()

main()
 
