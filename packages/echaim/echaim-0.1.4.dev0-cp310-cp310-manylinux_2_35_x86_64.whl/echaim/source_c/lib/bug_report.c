//
// Created by lap1dem on 17/11/22.
//

#include "ECHAIM.h"
#include <stdio.h>
#include "errorCodes.h"

void print_d_array(double *arr, int len) {
    for (int j = 0; j < len; j++) {
        printf("%4.3e ", arr[j]);
    }
    printf("\n");
}

int main(){
    double lat[2] = {60,44}; //geographic latitude
    double lon[2] = {210,220}; //geographic longitude
    double altProfile[10] = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000}; //altitude (km) (for profile)
    double y[2]= {1996,2012}; //year
    double m[2] = {8,2}; //month
    double d[2]={21,12}; //day
    double h[2]={5,16}; //hour
    double mi[2]={0,11}; //minute
    double s[2]={0,0}; //second
    int l0 = 2; //lat/lon/time array size
    int l1 = 10; //alt array size
    char **er; //error output

    double **output;
    double ** output1, ** output2;
    int storm = 0; //storm perturbation flag
    int precip = 1; //precipitation model flag
    int dregion = 0; //d region model flag
    //Ask the model to log possible error codes
    logErrors(l0);

//    Expected output (copied from expectedOutput.txt)
    double expout_1[10] = {12367606066.263021, 108297932864.252319, 158962061260.812408, 73773659026.466248,
                           39244380430.132393, 24244371947.660633, 16552247379.927717,
                           12071804966.952993, 9210135282.446226, 7254833783.452740};
    double expout_2[10] = {4889714776.171849, 94811918511.811340, 336738565496.773254, 133293965021.893005,
                           64477786540.683990, 38014163185.852394, 25242375055.590450,
                           18037499384.225201, 13520205967.189016, 10471259495.144081};

//    Batch calculation
    output = densityProfile(lat, lon, y, m, d, h, mi, s, storm, precip, dregion, l0, altProfile, l1, 0);

//    Single calculation
    output1 = densityProfile(&lat[0], &lon[0], &y[0], &m[0], &d[0], &h[0], &mi[0], &s[0], storm, precip, dregion, 1, altProfile, l1, 0);
    output2 = densityProfile(&lat[1], &lon[1], &y[1], &m[1], &d[1], &h[1], &mi[1], &s[1], storm, precip, dregion, 1, altProfile, l1, 0);

    printf("=========== FIRST COORDINATE ============\n");
    printf("Expected output:\t");
    print_d_array(expout_1, l1);
    printf("Batch calculation:\t");
    print_d_array(output[0], l1);
    printf("Single calculation:\t");
    print_d_array(output1[0], l1);

    printf("=========== SECOND COORDINATE ============\n");
    printf("Expected output:\t");
    print_d_array(expout_2, l1);
    printf("Batch calculation:\t");
    print_d_array(output[1], l1);
    printf("Single calculation:\t");
    print_d_array(output2[0], l1);

}
