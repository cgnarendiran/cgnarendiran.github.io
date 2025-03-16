---
layout: project
title:  Remote Photoplethysmography using NIR Images
date:   2024-08-01
image:  images/project11/cover.png
tags:   rPPG NIR heart-rate monitoring computer-vision deep-learning automotive Mercedes-Benz
---
*On the cover: (a) NIR images to signal, (b) Principles of remote PhotoPlythesmoGraphy (rPPG)*

This work was conducted at Mercedes-Benz Research and Development. The project aimed to develop a robust, non-contact method for heart rate monitoring using Near-Infrared (NIR) imaging specifically designed for automotive environments.

## Background:
Remote Photoplethysmography (rPPG) enables contactless measurement of vital signals (majorly heart rate) by detecting subtle changes in skin reflectance that correspond to blood volume variations during cardiac cycles. While conventional PPG requires direct skin contact with sensors, rPPG leverages camera technology to extract the same physiological signals from a distance.

Most existing rPPG methods rely on RGB cameras and operate on the principle that hemoglobin absorption varies across different wavelengths of visible light. However, these approaches face significant challenges in automotive environments:

- Varying ambient lighting conditions (bright sunlight, night time, shadows, tunnels)
- Motion artifacts from vehicle vibrations and driver movements
- Limited processing resources on automotive-grade hardware

NIR imaging (wavelengths 700-1000nm) offers a promising alternative as it penetrates deeper into skin tissue, is less affected by ambient light variations, and can operate effectively in low-light conditions. Additionally, many modern vehicles already incorporate NIR cameras for driver monitoring systems, making integration more feasible. However, the signal-to-noise ratio in NIR is 1/10th compared to RGB making it a non-trvial and challenging problem.

## Methodology
#### 1. Data Collection and Ground Truth:
I designed a comprehensive data collection protocol that included:

- Custom NIR camera setup (940nm) installed in test vehicles
- Synchronized medical-grade ECG devices for ground truth heart rate
- Controlled driving scenarios (still, running engine, driving)
- Diverse subject pool (varying age, gender, skin tone)
- Challenging conditions (sunglasses, facial hair, head movements)

The final dataset comprised of synchronized NIR video and ECG recordings from 500+ subjects across various driving conditions.

#### 2. Model Building Approach:
Initially, we attempted an end-to-end deep learning approach that directly regressed from NIR images to PPG signals. However, this proved challenging as the models severely overfit on the noisy automotive data. We then developed a more robust multi-stage pipeline.

The preprocessing stage focused on facial landmark detection using a specialized NIR face detection model. These landmarks were then used to fit a 3D facial mesh using MediaPipe, providing dense facial geometry. To obtain more accurate landmarks and head pose information, we solved the Perspective-n-Point (PnP) problem using the 3D mesh and camera parameters. The PnP solution provided both additional landmarks and transformation vectors that helped quantify subject motion.

From the detected landmarks, we extracted $\mathcal{P}$ distinct face patches that were likely to contain strong pulse signals. These patches included regions like the forehead, cheeks, and areas around major blood vessels. For each patch, we computed spatial pixel averages to reduce noise while preserving the underlying pulse signal. This resulted in $\mathcal{P}$ time-series signals that captured local blood volume variations. The extracted patch signals were then fed into a neural network architecture for PPG signal regression.

The networks were trained to map the $\mathcal{P}$ patch signals to clean PPG waveforms, with the ground truth coming from medical-grade ECG devices. The motion vectors obtained from PnP were used as additional inputs to help the network compensate for movement artifacts.


The final system achieved robust performance across various automotive conditions while maintaining computational efficiency suitable for real-time operation on vehicle hardware.

## Results:
The NIR-based rPPG system has it's own limitation. The following were the common failure cases:
- Small but consistent head movements (due to engine vibrations)
- Extreme voluntary head movements (>45° rotation)
- Very low lighting conditions (<5 lux)
- Certain facial characteristics affecting signal quality (very thick facial hair)

## Applications:
The developed technology enables several applications in automotive environments:

1. **Driver Monitoring Systems**: Integration with existing DMS to detect stress, fatigue, or medical emergencies
2. **Personalized Comfort**: Adjusting vehicle parameters (temperature, music, lighting) based on physiological state
3. **Health and Wellness**: Providing drivers with insights about cardiovascular health during commutes
4. **Autonomous Vehicle Handover**: Assessing driver readiness during transitions between autonomous and manual driving

## Conclusion:
This project successfully demonstrated the feasibility and advantages of using NIR imaging for reliable, non-contact heart rate monitoring in automotive environments. The approach overcomes many limitations of RGB-based methods and shows promise for integration into future vehicle health monitoring systems.

The combination of traditional signal processing techniques with deep learning approaches yielded robust performance across various challenging conditions typical in automotive scenarios. The technology has been incorporated into Mercedes-Benz's driver monitoring research platform and continues to be developed for potential production implementation.

**Further project details and code base are not revealed since the work is under NDA** 