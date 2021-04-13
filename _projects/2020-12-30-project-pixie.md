---
layout: project
title:  Project Pixie
date:   2020-12-30
image:  images/project8/cover.png
tags:   pixie autonomous robotics nvidia isaac ros segmentation croprow 
---
*On the cover: Robot Pixie in front of de campus Almkerk*

This work done at PixelFarmingRobotics BV. (client of CBoost BV. Inc.). The aim of the project is to make a four wheeled drive completely autonomous using the sensors on board.  

The robot Pixie was designed to have logistics applications in an agriculture field that includes carrying tools to the bigger robot (Robot One), transporting food produce and several auxilliary tasks on the farm. 

Robot Pixie was built with the following hardware:
1. Four-wheeled, chassis with adjustable belt tension mechanism
2. Two Intel D415 infrared stereo depth and RGB cameras (front and back)
3. Two Nemamotors and their motor drivers
4. STM microcontroller for serial communication with the drivers
5. Nvidia Jetson AGX Xavier for all the computations
6. Neopixel LED strips with arduino for robot state indication
7. Lithium Phosphate battery pack and voltage converters 
8. WiFi module

The robot is built to be completely autonomous with several capabilities to function on a farm field. For sensor communication and networking, we use the open source [Nvidia Isaac 2020.2](https://docs.nvidia.com/isaac/isaac/doc/index.html). This platform is quite similar to ROS except with Nvidia's own libraries for several robot functionalities; well suited for Jetson devices and is thus production ready. Isaac provides the platform to bundle functional code in the form of codelets that are modular and can be compiled with required dependencies. All the necessary nodes and their edges can be defined as an application graph that can be spawned at run time of the robot. Isaac SDK comes with toolchains based on the Bazel build system for building and deploying applications. The navigation pipeline which is responsible for rendering Pixie autonomous, has several moving parts. This includes the localization, local & global mapping (costmaps), goal setting, local & global path planning and control. 

There are several unique features to Pixie as follows: The stereo vision information is used for publishing the odometry and directly used for localization since it is more robust than flatscan based localization in an open farm. In order to account for drifting, we used relocalization based on AprilTags that are printed and placed across the field. Visibility Graph Algorithm (VGA) is used to determine the global path in an occupancy map and Linear Quadratic Regulator (LQR) provides local trajectory plan using the odometry and global plan from VGA. The trajectories are converted to linear and angular velocity commands and sent to a Differential drive controller. Since it's a four wheeled drive, additional constraints were included to make the steering smooth. The control commands are read from the buffer and are converted to motor wheel speeds for a differential drive. An available map with preset goals of the field is extracted from server by a client call codelet and loaded dynamically as required. The following capabilities were added for Pixie:

1. 3D Pointcloud depth flattening to flatscans for obstacle avoidance
2. AprilTag relative position detection using RGB camera
3. Robot relocalization using AprilTags and when the tracker is lost
3. Steering constraints, max speed constraints, setting speeds and acc. through serial communication with STM
4. Stereo Visual Odometry calculations (position obtained from ELBRUS algorithm Isaac) 
5. Neopixel LEDs lighting reflecting robot state
6. Process the waypoints and global map from server for dynamic goal setting


![alt](/images/project8/1.jpg)
*Working on the farm field at de campus Almkerk. The small robot behind us is Pixie and the large one at the back is Robot One*

**Further project details and code base are not revealed since the work is under NDA**
