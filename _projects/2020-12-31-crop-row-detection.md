---
layout: project
title:  Crop Row Detection pipeline
date:   2020-12-31
image:  images/project9/cover.png
tags:   pixie autonomous robotics nvidia isaac ros segmentation croprow 
---
*On the cover: Final results after segmentation by SegNet and HoughCNet followed by probabilistic Hough Line Transform on a sample Bean field image*

This work is done at PixelFarmingRobotics BV. (client of CBoost BV. Inc.). The aim of the project is to produce a robust crop row detection pipeline that can extract crop rows from an image feed. This pipeline is then deployed and used on *Pixie* and *Robot One* to help in autonomous guided navigation on the field.

Due to the nature of the dataset and the usage of image processing techniques, the task poses several challenges:
1. Weed infestation
2. Various POVs (top view/ horizon view)
3. Lighting/noise conditions
4. Different growth stages of the crop (for segmentation)

The task of crop row detection can be divided into two sub-problems:
1. Segmentation of crops (distinguish the crop from the soil and weed)
2. Line Detection of the major crop rows (using the above segmentation results)

Two appraoches were considered for the whole task: OpenCV algorithms and Deep learning techniques. The pros and cons were considered for each technique and the best method was chosen for each sub-problem.

![alt](/images/project9/1.png)
*OpenCV and Deep Learning techniques for the sub-problems*

## Data:
Data labeling is a huge bottleneck. Several open-source online annotation tools were considered for the task, but they lack the features of a paid tool and are poor/less supported or simply have less features. Even with open-source tools, we needed some additional pre-processing. Hence we adopted a preliminary HSV masking in OpenCV followed by weed removal manually in Gimp. 

Two datasets were available for the project:
1. Target data: TOGBeanField images (propreitary, aerial view, 72 images, no labels)
2. For proof of concept: [Weedmap](https://www.mdpi.com/2072-4292/10/9/1423) An open source data of a maize field (aerial view, 176 images, labels available)

![alt](/images/project9/2.png)
*Segmentation result of SegNet on Weedmap data*

The results were promising on TOGBeanField with an IOU score of 0.87 by applying both SegNet and HoughCNet in succession and taking an intersection of the predicted areas. The ML code was written in PyTorch Lightning, trained using an augmented dataset and tested on part of the dataset (10%). The trained model was then deployed on the robot as a codelet in Isaac 2020.2 on the Jetson Xavier AGX and at inference uses TensorRT to increase performance.

**Further project details and code base are not revealed since the work is under NDA**
