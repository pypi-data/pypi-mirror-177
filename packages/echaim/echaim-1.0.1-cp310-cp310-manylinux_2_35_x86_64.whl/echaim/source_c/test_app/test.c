//
// Created by lap1dem on 28/10/22.
//

#include <stdio.h>
#include <string.h>
#include <omp.h>
#include "../lib/sqlite3.h"
#include "../lib/global.h"
#include "../lib/date.h"
#include "../lib/getIndices.h"
//#include "../lib/ECHAIM.h"
#include <time.h>
#include <stdlib.h>


void print_d_array(double *arr, int len) {
    for (int j = 0; j < len; j++) {
        printf("%f ", arr[j]);
    }
    printf("\n");
}


int main(){
    strcpy(DIR, "/home/lap1dem/dev-python/echaim/src/echaim/model_data/");
//    sqlite3 *db, *dbCoefs;
//    strcpy(cwd,DIR);
//    strcat(cwd,"CHAIM_DB.db");
//    int rc = sqlite3_open(cwd, &db);
//    if (rc) {printf("Error: CHAIM_DB could not be opened\n");}

    double jd1 = julianDate(2020, 2, 13, 6, 20, 0);
    double jd2 = julianDate(2020, 3, 13, 6, 20, 0);
    double *x;
    int *lx;

    int nthreads, tid;
//    printf("%d", sqlite3_threadsafe());
    nthreads = omp_get_num_threads();
    int N = 50000;
    double * output = calloc(N, sizeof(double));

    int NTHREADS = 16;



    clock_t start = clock();
    double start_omp = omp_get_wtime();

    #pragma omp parallel for default(none) shared(jd1, jd2, DIR, N, output) private(x, lx, nthreads, tid) num_threads(NTHREADS)
    for (int i=0; i < N; i++) {
        sqlite3 *db;
        char cwd[1024];
        strcpy(cwd, DIR);
        strcat(cwd,"CHAIM_DB.db");
        sqlite3_open(cwd, &db);
        tid = omp_get_thread_num();
//        printf("Thread = %d\n", tid);
        output[i] = F10_81(jd1 - i, jd2 - i, &x, &lx, db)[0];
    }

    clock_t stop = clock();
    double stop_omp = omp_get_wtime();
    print_d_array(output, 10);
    double elapsed = (double) (stop - start) / CLOCKS_PER_SEC;
    printf("\nCumulative thread time: %.5f\n", elapsed);
    printf("\nWall time: %.5f\n", stop_omp-start_omp);

    return 0;
};
