project(main)
cmake_minimum_required(VERSION 3.2)
set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)


include_directories("${PROJECT_SOURCE_DIR}/inc")

aux_source_directory("${PROJECT_SOURCE_DIR}/src" SRC_LIST)

add_executable(main main.c ${SRC_LIST})
