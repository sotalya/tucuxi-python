cmake_minimum_required(VERSION 3.15...3.27)
project(sotalya LANGUAGES CXX)

# Common part for every modules that uses CMake
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=0)

if(SKBUILD)
  set(Python_EXECUTABLE "${PYTHON_EXECUTABLE}")
  set(Python_INCLUDE_DIR "${PYTHON_INCLUDE_DIR}")
  set(Python_LIBRARY "${PYTHON_LIBRARY}")
endif()

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

execute_process(COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ECHO STDOUT
  ECHO_OUTPUT_VARIABLE
  ECHO_ERROR_VARIABLE
  )
  
set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(PYBIND11_FINDPYTHON ON)

if (WIN32)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /UMBCS /D_UNICODE /DUNICODE")
elseif (APPLE)
    add_definitions(-DUNIX)
    # enable c++17
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
    add_compile_options(-Wno-deprecated-declarations)
else (UNIX)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -fsplit-stack -fno-lto -g")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -fsplit-stack -fno-lto -g")
endif (WIN32)

set(Boost_USE_MULTITHREADED      ON)
set(Boost_USE_STATIC_RUNTIME    OFF)

# tucuxi-core sources (they ned to be defined once only, for every modules that uses them)
set(TUCUCORE_SRC ${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/src/)
set(TUCUCORE_LIBS ${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/libs/)

set(BOOST_ROOT ${TUCUCORE_LIBS}/boost)
set(FRUCTOSE_ROOT ${TUCUCORE_LIBS}/fructose)
set(SPDLOG_ROOT ${TUCUCORE_LIBS}/spdlog)
set(EIGEN_ROOT ${TUCUCORE_LIBS}/eigen)
set(DATE_ROOT ${TUCUCORE_LIBS}/date)
set(RAPIDXML_ROOT ${TUCUCORE_LIBS}/rapidxml)
set(RAPIDJSON_ROOT ${TUCUCORE_LIBS}/rapidjson)
set(BOTAN_ROOT ${TUCUCORE_LIBS}/botan)
set(CXXOPTS_ROOT ${TUCUCORE_LIBS}/cxxopts)
set(TINYJS_ROOT ${TUCUCORE_LIBS}/tiny-js)

include_directories(
				${TUCUCORE_SRC}
        ${BOOST_ROOT}
        ${EIGEN_ROOT}
        ${FRUCTOSE_ROOT}/include
        ${SPDLOG_ROOT}/include
        ${DATE_ROOT}/include
        ${RAPIDXML_ROOT}
        ${RAPIDJSON_ROOT}/include
        ${BOTAN_ROOT}/build/include
        ${CXXOPTS_ROOT}/include
        ${TINYJS_ROOT})

set(TINYJS_SOURCES ${TINYJS_ROOT}/TinyJS.cpp
        ${TINYJS_ROOT}/TinyJS_Functions.cpp
        ${TINYJS_ROOT}/TinyJS_MathFunctions.cpp)

add_library(tinyjs STATIC ${TINYJS_SOURCES})

set(COMMON_DIR ${TUCUCORE_SRC}/tucucommon)
set(TUCUXICOMMON_SOURCES
        ${COMMON_DIR}/componentmanager.cpp
        ${COMMON_DIR}/datetime.cpp
        ${COMMON_DIR}/duration.cpp
        ${COMMON_DIR}/iimport.cpp
        ${COMMON_DIR}/jsengine.cpp
        ${COMMON_DIR}/logger.cpp
        ${COMMON_DIR}/timeofday.cpp
        ${COMMON_DIR}/translatablestring.cpp
        ${COMMON_DIR}/unit.cpp
        ${COMMON_DIR}/utils.cpp
        ${COMMON_DIR}/xmlattribute.cpp
        ${COMMON_DIR}/xmldocument.cpp
        ${COMMON_DIR}/xmlimporter.cpp
        ${COMMON_DIR}/xmlnode.cpp)

add_library(tucuxicommon STATIC ${TUCUXICOMMON_SOURCES})

set(CORE_DIR ${TUCUCORE_SRC}/tucucore)
set(TUCUXICORE_SOURCES
        ${CORE_DIR}/aposteriorietascalculator.cpp
        ${CORE_DIR}/cachecomputing.cpp
        ${CORE_DIR}/cachedexponentials.cpp
        ${CORE_DIR}/computingadjustments.cpp
        ${CORE_DIR}/computingcomponent.cpp
        ${CORE_DIR}/computingrequestxmlexport.cpp
        ${CORE_DIR}/computingutils.cpp
        ${CORE_DIR}/concentrationcalculator.cpp
        ${CORE_DIR}/covariateevent.cpp
        ${CORE_DIR}/covariateextractor.cpp
        ${CORE_DIR}/cyclestatisticscalculator.cpp
        ${CORE_DIR}/cyclestatistics.cpp
        ${CORE_DIR}/dosage.cpp
        ${CORE_DIR}/drugdomainconstraintsevaluator.cpp
        ${CORE_DIR}/drugfilevalidator.cpp
        ${CORE_DIR}/drugmodelchecker.cpp
        ${CORE_DIR}/drugmodelimport.cpp
        ${CORE_DIR}/drugmodelrepository.cpp
        ${CORE_DIR}/generalextractor.cpp
        ${CORE_DIR}/hardcodedoperation.cpp
        ${CORE_DIR}/intakeevent.cpp
        ${CORE_DIR}/intakeextractor.cpp
        ${CORE_DIR}/intakeintervalcalculatoranalytical.cpp
        ${CORE_DIR}/intakeintervalcalculator.cpp
        ${CORE_DIR}/intakeintervalcalculatorrk4.cpp
        ${CORE_DIR}/intaketocalculatorassociator.cpp
        ${CORE_DIR}/likelihood.cpp
        ${CORE_DIR}/montecarlopercentilecalculator.cpp
        ${CORE_DIR}/multicomputingadjustments.cpp
        ${CORE_DIR}/multicomputingcomponent.cpp
        ${CORE_DIR}/multiconcentrationcalculator.cpp
        ${CORE_DIR}/multilikelihood.cpp
        ${CORE_DIR}/multimontecarlopercentilecalculator.cpp
        ${CORE_DIR}/operablegraphmanager.cpp
        ${CORE_DIR}/operation.cpp
        ${CORE_DIR}/overloadevaluator.cpp
        ${CORE_DIR}/parameter.cpp
        ${CORE_DIR}/parametersextractor.cpp
        ${CORE_DIR}/pkmodel.cpp
        ${CORE_DIR}/residualerrormodel.cpp
        ${CORE_DIR}/residualerrormodelextractor.cpp
        ${CORE_DIR}/sampleevent.cpp
        ${CORE_DIR}/sampleextractor.cpp
        ${CORE_DIR}/targetevaluationresult.cpp
        ${CORE_DIR}/targetevaluator.cpp
        ${CORE_DIR}/targetevent.cpp
        ${CORE_DIR}/targetextractor.cpp
        ${CORE_DIR}/treatmentdrugmodelcompatibilitychecker.cpp
        ${CORE_DIR}/validvalues.cpp
        ${CORE_DIR}/version.cpp
        ${CORE_DIR}/computingservice/computingaborter.cpp
        ${CORE_DIR}/computingservice/computingrequest.cpp
        ${CORE_DIR}/computingservice/computingresponse.cpp
        ${CORE_DIR}/computingservice/computingresult.cpp
        ${CORE_DIR}/computingservice/computingtrait.cpp
        ${CORE_DIR}/computingservice/icomputingservice.cpp
        ${CORE_DIR}/drugmodel/activemoiety.cpp
        ${CORE_DIR}/drugmodel/analyte.cpp
        ${CORE_DIR}/drugmodel/drugmodel.cpp
        ${CORE_DIR}/drugmodel/drugmodeldomain.cpp
        ${CORE_DIR}/drugmodel/drugmodelmetadata.cpp
        ${CORE_DIR}/drugmodel/errormodel.cpp
        ${CORE_DIR}/drugmodel/formulationandroute.cpp
        ${CORE_DIR}/drugmodel/parameterdefinition.cpp
        ${CORE_DIR}/drugmodel/targetdefinition.cpp
        ${CORE_DIR}/drugmodel/timeconsiderations.cpp
        ${CORE_DIR}/drugmodel/validdose.cpp
        ${CORE_DIR}/drugmodel/validduration.cpp
        ${CORE_DIR}/drugtreatment/drugtreatment.cpp
        ${CORE_DIR}/drugtreatment/sample.cpp
        ${CORE_DIR}/drugtreatment/target.cpp
        ${CORE_DIR}/pkmodels/onecompartmentbolus.cpp
        ${CORE_DIR}/pkmodels/onecompartmentextra.cpp
        ${CORE_DIR}/pkmodels/onecompartmentextralag.cpp
        ${CORE_DIR}/pkmodels/onecompartmentinfusion.cpp
        ${CORE_DIR}/pkmodels/rkmichaelismentenenzyme.cpp
        ${CORE_DIR}/pkmodels/rkmichaelismentenonecomp.cpp
        ${CORE_DIR}/pkmodels/rkmichaelismententwocomp.cpp
				${CORE_DIR}/pkmodels/rkmichaelismententwocompvmaxamount.cpp
        ${CORE_DIR}/pkmodels/rkonecompartmentextra.cpp
        ${CORE_DIR}/pkmodels/rkonecompartmentgammaextra.cpp
        ${CORE_DIR}/pkmodels/rktwocompartmenterlang.cpp
        ${CORE_DIR}/pkmodels/rktwocompartmentextralag.cpp
        ${CORE_DIR}/pkmodels/threecompartmentbolus.cpp
        ${CORE_DIR}/pkmodels/threecompartmentextra.cpp
        ${CORE_DIR}/pkmodels/threecompartmentinfusion.cpp
        ${CORE_DIR}/pkmodels/twocompartmentbolus.cpp
        ${CORE_DIR}/pkmodels/twocompartmentextra.cpp
        ${CORE_DIR}/pkmodels/twocompartmentextralag.cpp
        ${CORE_DIR}/pkmodels/twocompartmentinfusion.cpp)

add_library(tucuxicore STATIC ${TUCUXICORE_SOURCES})

set(QUERY_DIR ${TUCUCORE_SRC}/tucuquery)
set(TUCUXIQUERY_SOURCES
        ${QUERY_DIR}/administrativedata.cpp
        ${QUERY_DIR}/computingquery.cpp
        ${QUERY_DIR}/computingqueryresponse.cpp
        ${QUERY_DIR}/computingqueryresponsexmlexport.cpp
        ${QUERY_DIR}/computingresponseexport.cpp
				${QUERY_DIR}/fullsample.cpp
        ${QUERY_DIR}/parametersdata.cpp
        ${QUERY_DIR}/querycomputer.cpp
        ${QUERY_DIR}/querydata.cpp
        ${QUERY_DIR}/queryimport.cpp
        ${QUERY_DIR}/querylogger.cpp
        ${QUERY_DIR}/querytocoreextractor.cpp
        ${QUERY_DIR}/requestdata.cpp)

add_library(tucuxiquery STATIC ${TUCUXIQUERY_SOURCES})

# Module CMakeList file
include(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/pycli/CMakeLists.txt)

