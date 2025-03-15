---
layout: project
title:  Fixedwing swarming
date:   2020-12-31
image:  images/project10/cover.png
tags:   fixedwing swarming robotics ros ros2 collision avoidance uav 
---
*On the cover: Four fixedwing UAVs swarming on QGCS (QGround Control Station, by PX4)*

This work is done at NewSpace Research and Technologies. The aim of the project is to build the software stack from ground up for a swarm of fixedwing UAVs. This includes the control, guidance, collision avoidance, scheduling and communication.

## Hardware:
For this project, a [Talon](https://runrc.in/product/x-uav-talon-epo-1718mm-wingspan-v-tail-fpv-plane-aircraft-kit-v3/) UAV (bird) is used as the base aircraft frame for the flight tests. An onboard computer (Raspberry Pi4) is set up along with the firmware (Pixhawk Cube Orange) in the body of the aircraft. All the sensors including the BMP 180 barometer, s 1000KV brushless motors for throttle, SG90 servos for control surfaces, Here3 GPS GNSS and MS 4525DO Airspeed Sensor with pitot tube are attached to PixCube on the UAV. A telemetry conection is established between PixCube and RPi & PixCube and Modem. The RPi and modem are connected by Ethernet. Any communication to the bird happens via the modem which is set to have a multicast network.

Direct controls to the firmware of the bird can be achieved either by using a Remote Control (eg. FlySky FS-i6 RC) or the [PX4](https://px4.io/) based [QGCS](http://qgroundcontrol.com/) software. The RC and the QGCS can be used to change the mode (LOITER, AUTO, MANUAL, LAND, etc.) of the UAV and send pre-planned missions.

## Software:
In this project, ROS (Robot Operating System) is used as a middleware for communication betweeen the various software modules inside the RPi. ROS2 is used for inter-drone communication. This project is written using C++ and Python. 

![alt](/images/project10/comm_architecture.png)
*Communication architecture for fixedwing swarming*

The whole software stack can be divided into the following modules:
1. FS-GCS
2. Communication
3. Scheduler
4. Guidance
5. Collision avoidance
6. PX4-Mavros

The in-house built Fixedwing Swarming Ground Control Station aka *FS-GCS* is a custom made GCS suited for NewSpace's fixedwing swarm needs. This is explained in a separate project post. As for the various communications, different protocols and middlewares are used between the GCS happens via json messages. Communication to the firmware happens via [MAVROS](http://wiki.ros.org/mavros) that converts ROS based messages to [MAVLink](https://mavlink.io/en/) messages to be sent to PX4. 

Communication between the RPis and the FS-GCS happens via [ROS2](https://docs.ros.org/en/foxy/index.html). ROS2 is chosen here as it doesn't use master-slave protocol and hence avoids the single point of failure. Communication between ROS1 and ROS2 happens via [ROS1_bridge](https://github.com/ros2/ros1_bridge). Since the FS-GCS is entirely written in python, a flask server runs that connects the GCS to the ROS2 nodes. 

The Scheduler modules are responsible for keeping track of completion of routines and determining the triggering of next routine that the birds have to follow. For example, comparison of flock timers between the planes and ending the flock when the first plane completes the flock. 

The Guidance modules implement the [Beard and McLain's](https://github.com/randybeard/uavbook) flight guidance laws. It that take as input the waypoints and convert them into the desired velocity, desired altitude and desired course of the planes at each instant. This module consists of the path planner, path manager and path follower. The path planner computes the course angle to be followed at any waypoint and adds additional information to complete any kind of routines. The path manager computes the [Dubin's path](http://planning.cs.uiuc.edu/node821.html) given these waypoints. The Dubin's paths consists of stright lines and orbital paths. The path follower then computes the desired heading, velocity and course given this information.

The Collision avoidance module takes the above input and extracts the collision free velocities using the RVO2 library. All the computations happen in the NED (North East Down) coordinate frames. When a plane disconnects from the network, it is sent to infinity. 

The PX4-MAVROS module is responsible for NED to ENU frame conversions (as MAVROS works with the ENU frame) and communication between the collision avoidance module and PX4. The desired commands are being sent to the PX4 and in turn the state feedback message is received, parsed and shared with the rest of the pipeline. 


**Further project details and code base are not revealed since the work is under NDA**
