cmake_minimum_required(VERSION 3.15...3.27)
project(sotalya LANGUAGES CXX)

# Common part for every modules that uses CMake
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=0)

# Language
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Python configs
if(SKBUILD)
  set(Python_EXECUTABLE "${PYTHON_EXECUTABLE}")
  set(Python_INCLUDE_DIR "${PYTHON_INCLUDE_DIR}")
  set(Python_LIBRARY "${PYTHON_LIBRARY}")
endif()

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Pybind11 configs
execute_process(COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
  COMMAND_ECHO STDOUT
  ECHO_OUTPUT_VARIABLE
  ECHO_ERROR_VARIABLE
  )
  
set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
set(PYBIND11_FINDPYTHON ON)

# Config Compiler
add_definitions(-DUNICODE)
add_definitions(-D_UNICODE)

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

# Set boost options
set(Boost_USE_MULTITHREADED      ON)
set(Boost_USE_STATIC_RUNTIME    OFF)

# tucuxi-core sources (they ned to be defined once only, for every modules that uses them)
include(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/libs/tucuxi-core_libs)
# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/libs/tiny-js tiny-js)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/src/tucucommon tucucommon)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/src/tucucore tucucore)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/src/tucuquery tucuquery)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/tucuxi-core/src/)

# Module CMakeList file
include(${CMAKE_CURRENT_SOURCE_DIR}/sotalya/pycli/CMakeLists.txt)

