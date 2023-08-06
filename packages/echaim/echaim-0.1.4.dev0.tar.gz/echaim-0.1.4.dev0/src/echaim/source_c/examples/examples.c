#include <stdio.h>
#include <stdlib.h>
#include "ECHAIM.h"
#include "errorCodes.h"

//****DEBUGGING************
#ifdef DBG
#include "memwatch.h"
#endif
//*************************

void main()
{
	
	//declared inputs
	double lat[2] = {60,44}; //geographic latitude
	double lon[2] = {210,220}; //geographic longitude
	double altProfile[10] = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000}; //altitude (km) (for profile)
	double altPath[2] = {200, 210}; //altitude (km) (for path)
	double y[2]= {1996,2012}; //year
	double m[2] = {8,2}; //month
	double d[2]={21,12}; //day
	double h[2]={5,16}; //hour
	double mi[2]={0,11}; //minute
	double s[2]={0,0}; //second
	int l0 = 2; //lat/lon/time array size
	int l1 = 10; //alt array size
	char **er; //error output
	
	
	//Function to update the local DB file
	//Inputs: 0 = check if update is necessary, 1 = force an update.
	int rc = updateLocalDB(0);
	
	//Check when the DB was last updated
	double dbDate = getDBDate();
	printf("The DB was updated on Julian Date %f\n", dbDate);
	
	/*Inputs correspond to:
	August 21, 1996, at 5 hours UTC at location 60 N 210 E
	February 12, 2012, 16 hours and 11 minutes UTC at location 53 N 220 E
	
	/******************************************
	Calculate NmF2 and print the results
	Takes latitude, longitude, year, month,
	day, hour, minute, and seconds as inputs (double arrays/pointer)
	final input is the integer length of the arrays
	all inputs should be the same length*/
	
	//Output is an array (pointer) of the NmF2 values with length of l0
	
	double *output;
	
	//Ask the model to log possible error codes
	logErrors(l0);

	printf("Now running NmF2 function \n");
	
	output = NmF2(lat, lon, y, m, d, h, mi, s, l0, 1);

	printf("Output of NmF2 function \n");
	
	for (int i=0; i<l0; i++) 
	{
		printf("%f\n", output[i]);
	}

	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}
	
	free(output);
	
	/******************************************
	Calculate NmF2 (with storm perturbation) and print the results
	Takes latitude, longitude, year, month,
	day, hour, minute, and seconds inputs (double arrays/pointer)
	final input is the integer length of the arrays
	all inputs should be the same length
	
	Output is an array (pointer) of the NmF2 values with length of l0*/
	
	//double *output;
	
	//Ask the model to log possible error codes
	logErrors(l0);
	
	printf("Now running NmF2Storm function \n");
	
	output = NmF2Storm(lat, lon, y, m, d, h, mi, s, l0, 0);

	printf("Output of NmF2Storm function \n");
	
	for (int i=0; i<l0; i++) 
	{
		printf("%f\n", output[i]);
	}
	
	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}

	free(output);
	
	/******************************************
	Calculate HmF2 and print the results
	Takes latitude, longitude, year, month,
	day, hour, minute, and seconds as inputs (double arrays/pointer)
	final input is the integer length of the arrays
	all inputs should be the same length
	
	Output is an array (pointer) of the HmF2 values with length of l0*/
	
	//double *output;
	
	//Ask the model to log possible error codes
	logErrors(l0);

	printf("Now running HmF2 function \n");
	
	output = HmF2(lat, lon, y, m, d, h, mi, s, l0, 0);

	printf("Output of HmF2 function \n");
	
	for (int i=0; i<l0; i++) 
	{
		printf("%f\n", output[i]);
	}
	
	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}

	free(output);
	
	/******************************************
	Calculate HmF1 and print the results
	Takes latitude, longitude, year, month,
	day, hour, minute, and seconds as inputs (double arrays/pointer)
	final input is the integer length of the arrays
	all inputs should be the same length
	
	Output is an array (pointer) of the HmF2 values with length of l0*/
	
	//double *output;
	
	//Ask the model to log possible error codes
	logErrors(l0);

	printf("Now running HmF1 function \n");
	
	output = HmF1(lat, lon, y, m, d, h, mi, s, l0, 0);

	printf("Output of HmF1 function \n");
	
	for (int i=0; i<l0; i++) 
	{
		printf("%f\n", output[i]);
	}
	
	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}

	free(output);
	
	/******************************************
	Calculate density profiles and print the results
	Takes latitude, longitude, year, month,
	day, hour, minute, seconds as inputs (double arrays/pointer)
	'storm' is an integer array (pointer) indicating which lat/lon/time
	sets are to be calculated with the storm perturbation
	if storm[i] != 0 then the storm calculation is used for set i
	l0 input is the integer length of the arrays
	these inputs should be the same length
	Next an altitude array (double pointer)
	followed by l1, the length of this array (int)
	
	Output is a double array (pointer) of the profiles a size of [l0,l1]
	eg output[0][0->l1-1] is the profile for the lat/lon/time pair at index 0*/
	
	double **output2;
	int storm = 0; //storm perturbation flag
	int precip = 1; //precipitation model flag
	int dregion = 0; //d region model flag
	//Ask the model to log possible error codes
	logErrors(l0);

	printf("Now running densityProfile function \n");
	
	output2 = densityProfile(lat, lon, y, m, d, h, mi, s, storm, precip, dregion, l0, altProfile, l1, 0);

	printf("Output of densityProfile function \n");
	
	for (int i=0; i<l0; i++) 
	{
		for (int j=0; j<l1; j++)
		{
			printf("%f ", output2[i][j]);
		}
	}
	
	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}

	for (int i=0; i<l0; i++) {free(output2[i]);}
	free(output2);
	
	/******************************************
	Calculate density paths and print the results
	Takes latitude, longitude, altitudes, year, month,
	day, hour, minute, seconds as inputs (double arrays/pointer)
	'storm' is an integer array (pointer) indicating which lat/lon/time
	sets are to be calculated with the storm perturbation
	if storm[i] != 0 then the storm calculation is used for set i
	l0 input is the integer length of the arrays
	these inputs should be the same length
	
	Output is a double array (pointer) of the densities, size of l0 */
	
	//double *output;
	precip = 0;
	storm = 1;
	
	//Ask the model to log possible error codes
	logErrors(l0);

	printf("Now running densityPath function \n");
	
	output = densityPath(lat, lon, altPath, y, m, d, h, mi, s, storm, precip, dregion, l0, 0);

	printf("Output of densityPath function \n");
	
	for (int i=0; i<l0; i++) 
	{
		printf("%f\n", output[i]);
	}
	
	//get and print the error codes
	er = getErrors();
	
	for (int i=0; i<l0; i++)
	{
		printf("Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
			er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
	}

	free(output);
	
}

