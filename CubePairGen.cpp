// Use Transition Density Cubes from Gaussian/MultiWfn to generate couplings - (c) Aleksey Kocherzhenko, 2016

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

FILE *fp;

// Read in the coordinates and values for cube elements
int getcubecoords(char *pinfile, double *px, double *py, double *pz, double *pvalue)
{
  int j, size;

  fp = fopen(pinfile, "r");
  fscanf(fp, " %d ", &size);
  for (j=0; j<size; j++)
  {
    fscanf(fp, "%lf %lf %lf %lf\n", px+j, py+j, pz+j, pvalue+j);
//    printf("%15.8lf %15.8lf %15.8lf %18.5le\n", px[j], py[j], pz[j], pvalue[j]);
  }
  fclose(fp);

  return size;
}


// Main program starts here
int main(int argc, char **argv)
{
  double *px1, *py1, *pz1, *pvalue1;
  double *px2, *py2, *pz2, *pvalue2;
  double coupling, distance;
  int size1, size2, i, j;

//  printf("Starting cubePairgen...\n");

  fp = fopen(argv[1], "r");
  fscanf(fp, " %d ", &size1);
  fclose(fp);
//  printf(" %d points in input file %s.\n", size1, argv[1]);

  fp = fopen(argv[2], "r");
  fscanf(fp, " %d ", &size2);
  fclose(fp);
//  printf(" %d points in input file %s.\n", size2, argv[2]);

  px1 = (double *) malloc(size1*sizeof(double)); py1 = (double *) malloc(size1*sizeof(double)); pz1 = (double *) malloc(size1*sizeof(double));
  pvalue1 = (double *) malloc(size1*sizeof(double));
  px2 = (double *) malloc(size2*sizeof(double)); py2 = (double *) malloc(size2*sizeof(double)); pz2 = (double *) malloc(size2*sizeof(double));
  pvalue2 = (double *) malloc(size2*sizeof(double));

// Get transition density cube (x, y, z coordinates and density values) from input files
  i = getcubecoords(argv[1], px1, py1, pz1, pvalue1);
  i = getcubecoords(argv[2], px2, py2, pz2, pvalue2);

  coupling = 0.0;

  for (i=0; i<size1; i++)
  {
    for (j=0; j<size2; j++)
    {
      distance = sqrt((px1[i]-px2[j])*(px1[i]-px2[j])+(py1[i]-py2[j])*(py1[i]-py2[j])+(pz1[i]-pz2[j])*(pz1[i]-pz2[j])); 
      coupling += pvalue1[i]*pvalue2[j]/distance;
    }
  }

  char num1[5], num2[5];
  strncpy(num1, &argv[1][8], 4); num1[4]='\0';
  strncpy(num2, &argv[2][8], 4); num2[4]='\0';
  
  printf("%s %s %10.6f \n", num1, num2, 14.3869*coupling/0.529);

  free(px1); free(py1); free(pz1); free(pvalue1);
  free(px2); free(py2); free(pz2); free(pvalue2);

//  printf("cubePairgen successfully finished!\n");

  return 0;
}

