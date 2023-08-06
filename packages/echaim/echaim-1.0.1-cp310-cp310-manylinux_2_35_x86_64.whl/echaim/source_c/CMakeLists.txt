cmake_minimum_required (VERSION 3.6.2)

set (project_name
	ECHAIM)

#Project name
project (${project_name})


#include_directories (../include)

#add_subdirectory(test_app/)

set(LIB_SOURCES
        lib/aacgmlib_v2.c
        lib/astalglib.c
        lib/calcBot.c
        lib/calcHmF1.c
        lib/calcMF2.c
        lib/calcPert.c
        lib/calcTop.c
        lib/date.c
        lib/densityFunc.c
        lib/densityPath.c
        lib/densityProfile.c
        lib/errorCodes.c
        lib/genmag.c
        lib/getCoefs.c
        lib/getDir.c
        lib/getIndices.c
        lib/getMagCoords.c
        lib/igrflib.c
        lib/mathlib.c
        lib/maxIndices.c
        lib/mlt_v2.c
        lib/otherIndices.c
        lib/parameterAE.c
        lib/parameterBot.c
        lib/parameterHmF1.c
        lib/parameterHmF2.c
        lib/parameterNmF2.c
        lib/parameterPert.c
        lib/parameterTop.c
        lib/prepInd.c
        lib/rtime.c
        lib/singleOutput.c
        lib/sqlite3.c
        lib/calcPrecip.c
        lib/ECHAIMFIRI2018.c
        lib/energyFluxModel.c
        lib/energyFunctions.c
        lib/FIRITools.c
        lib/getFIRI.c
        lib/getPrecipModel.c
        lib/nrlmsise-00_data.c
        lib/nrlmsise00.c
        lib/runNRLMSISE.c
        lib/updateLocalDB.c
        lib/python_api.c
	)


set_source_files_properties(lib/sqlite3.c PROPERTIES COMPILE_OPTIONS "-DSQLITE_THREADSAFE=2")

#create the shared library
add_library (${project_name} SHARED ${LIB_SOURCES})
#add_executable(ECHAIM_test test_app/test.c)

#Link the curl library
target_link_libraries(${project_name} curl)
#target_link_libraries(ECHAIM_test ${project_name} m)

#find_package(OpenMP)
#message("${OPENMP_FOUND}")
#if (OPENMP_FOUND)
#	set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
#	set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
#	set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
#endif()

#change the runtime output directory
get_filename_component(PARENT_DIR CMake DIRECTORY)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PARENT_DIR})

#set the compiler C99 flag
set_property(TARGET ${project_name} PROPERTY C_STANDARD 99)
