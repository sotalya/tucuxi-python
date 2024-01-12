cmake_minimum_required(VERSION 3.15...3.27)
project(_tucucore_wrapper LANGUAGES CXX)

add_compile_definitions(MODULE_NAME=${CMAKE_PROJECT_NAME})

set(WRAP_DIR ${CMAKE_CURRENT_SOURCE_DIR}/sotalya/pycli/tucupywrap)
set(TUCUPYWRAP_SOURCES
        ${WRAP_DIR}/wrapper.cpp
        ${WRAP_DIR}/wrapcomputer.cpp
        ${WRAP_DIR}/wraputils.cpp)

pybind11_add_module(${CMAKE_PROJECT_NAME} ${TUCUPYWRAP_SOURCES})

if (WIN32)
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE tucucore tucuquery tucucommon)
else (UNIX)
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE pthread tucucore tucuquery tucucommon)
endif (WIN32)

install(TARGETS ${CMAKE_PROJECT_NAME} DESTINATION ${CMAKE_INSTALL_PREFIX})