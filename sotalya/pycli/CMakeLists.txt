cmake_minimum_required(VERSION 3.15...3.27)
project(_tucucore_wrapper LANGUAGES CXX)

add_compile_definitions(MODULE_NAME=${CMAKE_PROJECT_NAME})

set(TUCUWRAP_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/sotalya/pycli)

set(WRAP_DIR ${TUCUWRAP_ROOT}/tucupywrap)
set(TUCUPYWRAP_SOURCES
        ${WRAP_DIR}/wrapper.cpp
        ${WRAP_DIR}/wrapcomputer.cpp
        ${WRAP_DIR}/wraputils.cpp)

pybind11_add_module(${CMAKE_PROJECT_NAME} ${TUCUPYWRAP_SOURCES})

if (WIN32)
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE tucuxicore tucuxiquery tucuxicommon tinyjs)
else (UNIX)
    target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE pthread tucuxicore tucuxiquery tucuxicommon tinyjs)
endif (WIN32)

install(TARGETS ${CMAKE_PROJECT_NAME} DESTINATION ${CMAKE_INSTALL_PREFIX})