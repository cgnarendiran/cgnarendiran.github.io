---
layout: project
title:  Remote Photoplethysmography using NIR Images
date:   2024-08-01
image:  images/project11/cover.jiff
tags:   rPPG NIR heart-rate monitoring computer-vision deep-learning automotive Mercedes-Benz
---
*On the cover: NIR camera setup for remote heart rate monitoring in an automotive environment*

This work was conducted at Mercedes-Benz Research and Development. The project aimed to develop a robust, non-contact method for heart rate monitoring using Near-Infrared (NIR) imaging specifically designed for automotive environments.

## Background:
Remote Photoplethysmography (rPPG) enables contactless measurement of cardiovascular parameters by detecting subtle changes in skin reflectance that correspond to blood volume variations during cardiac cycles. While conventional PPG requires direct skin contact with sensors, rPPG leverages camera technology to extract the same physiological signals from a distance.

Most existing rPPG methods rely on RGB cameras and operate on the principle that hemoglobin absorption varies across different wavelengths of visible light. However, these approaches face significant challenges in automotive environments:

- Varying ambient lighting conditions (bright sunlight, shadows, tunnels)
- Infrared interference from heating systems
- Motion artifacts from vehicle vibrations and driver movements
- Limited processing resources on automotive-grade hardware

NIR imaging (wavelengths 700-1000nm) offers a promising alternative as it penetrates deeper into skin tissue, is less affected by ambient light variations, and can operate effectively in low-light conditions. Additionally, many modern vehicles already incorporate NIR cameras for driver monitoring systems, making integration more feasible.

## Methodology:
The project was structured in three main phases:

### 1. Data Collection and Ground Truth:
I designed a comprehensive data collection protocol that included:

- Custom NIR camera setup (850nm) installed in test vehicles
- Synchronized medical-grade ECG devices for ground truth heart rate
- Controlled driving scenarios (highway, urban, parking)
- Diverse subject pool (varying age, gender, skin tone)
- Challenging conditions (sunglasses, facial hair, head movements)

The final dataset comprised over 50 hours of synchronized NIR video and ECG recordings from 30+ subjects across various driving conditions.

### 2. Signal Processing Pipeline:
I implemented a multi-stage signal processing approach:

- **Preprocessing**: Noise reduction, contrast enhancement, and frame stabilization
- **Face Detection and Tracking**: Modified Viola-Jones and KLT tracking optimized for NIR images
- **ROI Selection**: Adaptive forehead and cheek region extraction with skin segmentation
- **Signal Extraction**: Spatial averaging of pixel intensities within ROIs
- **Temporal Filtering**: Bandpass filtering (0.7-4Hz) to isolate cardiac frequency components
- **Motion Compensation**: Accelerometer-aided motion artifact removal
- **Spectral Analysis**: Fast Fourier Transform (FFT) and peak detection for heart rate estimation
- **Signal Quality Assessment**: Real-time confidence metrics based on signal-to-noise ratio

### 3. Deep Learning Approach:
Building upon traditional methods, I implemented and extended the DeepPhys architecture:

- **Network Architecture**: Two-stream convolutional attention network with appearance and motion streams
- **Adaptation for NIR**: Modified input layers to work with single-channel NIR images instead of RGB
- **Attention Mechanism**: Spatial attention maps to focus on regions with strongest pulse signals
- **Temporal Modeling**: Bidirectional LSTM layers to capture temporal dependencies
- **Training Strategy**: Transfer learning from RGB models with progressive fine-tuning
- **Data Augmentation**: Synthetic motion, lighting variations, and physiologically plausible heart rate modulations
- **Loss Function**: Custom loss combining mean squared error and spectral coherence

## Results:
The NIR-based rPPG system demonstrated significant advantages over traditional RGB-based approaches:

### Performance Metrics:
- **Mean Absolute Error (MAE)**: 3.2 BPM in controlled settings, 6.8 BPM in challenging scenarios
- **Pearson Correlation**: 0.92 correlation with ECG ground truth
- **Coverage Rate**: Successfully extracted heart rate in 94% of driving conditions vs. 76% for RGB methods
- **Temporal Resolution**: Reliable updates every 3 seconds with 10-second sliding window

### Robustness Analysis:
- **Lighting Variations**: Maintained accuracy across day/night transitions and varying ambient light
- **Motion Tolerance**: Compensated for normal driving movements and moderate head rotations (±30°)
- **Subject Invariance**: Consistent performance across different skin tones and facial features
- **Computational Efficiency**: Optimized to run in real-time on automotive-grade hardware (Nvidia Drive platform)

### Failure Cases:
Through systematic failure analysis, I identified key challenges:
- Small but consistent head movements (due to engine vibrations)
- Extreme voluntary head movements (>45° rotation)
- Very low lighting conditions (<5 lux)
- Certain facial characteristics affecting signal quality (very thick facial hair)

## Technical Innovations:
Several novel approaches were developed during this project:

1. **Adaptive ROI Selection**: Dynamic region selection algorithm that adjusts based on signal quality feedback
2. **Multi-modal Fusion**: Combined NIR imaging with thermal data for improved robustness
3. **Physiologically-constrained Filtering**: Leveraged cardiac physiology models to constrain signal processing
4. **Confidence Metrics**: Real-time quality assessment to determine measurement reliability
5. **Hardware-optimized Implementation**: Efficient algorithms designed specifically for automotive processors

## Applications:
The developed technology enables several applications in automotive environments:

1. **Driver Monitoring Systems**: Integration with existing DMS to detect stress, fatigue, or medical emergencies
2. **Personalized Comfort**: Adjusting vehicle parameters (temperature, music, lighting) based on physiological state
3. **Health and Wellness**: Providing drivers with insights about cardiovascular health during commutes
4. **Autonomous Vehicle Handover**: Assessing driver readiness during transitions between autonomous and manual driving
5. **Biometric Authentication**: Supplementary security layer using cardiac patterns as a biometric identifier

## Conclusion:
This project successfully demonstrated the feasibility and advantages of using NIR imaging for reliable, non-contact heart rate monitoring in automotive environments. The approach overcomes many limitations of RGB-based methods and shows promise for integration into future vehicle health monitoring systems.

The combination of traditional signal processing techniques with deep learning approaches yielded robust performance across various challenging conditions typical in automotive scenarios. The technology has been incorporated into Mercedes-Benz's driver monitoring research platform and continues to be developed for potential production implementation.

**Further project details and code base are not revealed since the work is under NDA** 