cmake_minimum_required(VERSION 3.5)
project(distro50ls)
add_subdirectory(libs/pybind11)
pybind11_add_module(distro50ls libs/distro50ls.cpp)