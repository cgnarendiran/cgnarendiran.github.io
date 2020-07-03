---
layout: project
title:  Autonomous Ground Vehicle - 13th in Global Competition on debut stint
date:   2017-09-01
image:  images/project4/cover.jpeg
tags:   cfi abhiyaan igvc
---
This project was started off at Center For Innovation (CFI, IITM) with the aim to understand and develop autonomous vehicles. We called us 'Team Abhiyaan' and represented IIT Madras in the 25th Annual International Ground Vehicle Competition (IGVC), one of the biggest unmanned ground vehicle competitions in the world for university students. This competition was held at Oakland University in Michigan, USA (2-5th June).

![alt](/images/project4/2.jpeg)
*Team picture*

On beahlf of my team I'm proud to convey that we placed in the top 13, amongst various international teams from different universities across the globe, in our debut in this competition. I was part of the software module in the team working towards integrating navigation stack and simulate the robot in a virtual physics environment. My work in the team as part of the software module is described:

Implementation of Navigation Stack: Written in ROS, capable of end to end GPS waypoint navigation. We use gmapping package to implement SLAM in a closed environment and outside spaces (provided enough obstacles to localize; dynamic obdtacle avoidance still requires SLAM). We further use move_base stack for internal costmap generation and DWA & TEB for path planning  algorithms. navsat_mapping for converting GPS co-ordiates to UTM and further to global map (specific to the robot) co-ordinates. 

![alt](/images/project4/1.jpeg)
*Gazebo Simulation of the robot*

Simulation using Gazebo: ​Constructed URDF and Xacro files as robot descriptors importing all the designed meshes of robotic components. Transmission tags are included to make the robot a differential drive. In-built gazebo plugins are added to specify the function of on-board sensors: LiDAR, IMU, encoders and camera. Lane detection by OpenCV is assisted by providing white lanes over ground for easy processing. Other capabilities such as teleop and controller interfaces are included while building the robot on the simulator.