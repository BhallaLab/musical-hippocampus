cmake_minimum_required(VERSION 2.8)
project(OpenDay)

find_package(OpenCV REQUIRED)

include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable(OpenDay ./main.cpp)

target_link_libraries(OpenDay ${OpenCV_LIBS})

