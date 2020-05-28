cmake_minimum_required(VERSION 2.8.3)
project(camcalib)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(

)

include_directories( ${catkin_INCLUDE_DIRS} )

catkin_install_python(PROGRAMS test/cam.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
