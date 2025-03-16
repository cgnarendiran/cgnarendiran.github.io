---
layout: project
title:  AI-Driven Quantitative Risk Analysis
date:   2025-02-16
image:  images/project12/cover.jpg
tags:   QRA P&ID PFD digitization computer-vision deep-learning oil-gas Aramco graph-algorithms
---
*On the cover: Digitized Process Flow Diagram (PFD) with highlighted Elementary Process Sections (EPS) and graph*

This work was conducted at Saudi Aramco. The project aimed to develop an automated system for digitizing Process Flow Diagrams (PFDs) and Piping and Instrumentation Diagrams (P&IDs) to enable efficient and accurate Quantitative Risk Analysis (QRA).

## Background:
In the oil and gas industry, Quantitative Risk Analysis is crucial for ensuring operational safety and regulatory compliance. Traditionally, this process involves manual interpretation of complex engineering diagrams such as P&IDs and PFDs, which is time-consuming, error-prone, and requires specialized expertise. These diagrams contain critical information about process equipment, instrumentation, and piping systems that form the basis for risk assessment.

The challenges with traditional manual approaches include:
- Inconsistent interpretation across different engineers
- Time-intensive process (weeks to months for large facilities)
- Difficulty in maintaining up-to-date risk assessments as facilities evolve
- Limited traceability between risk calculations and source documentation

Automating this process through AI and computer vision offers significant advantages in terms of speed, consistency, and accuracy, ultimately enhancing facility safety and operational efficiency.

## Methodology
#### 1. Document Detection and Recognition:
I developed a comprehensive detection system that included:

- **Multi-scale Object Detection**: Custom-trained YOLOv5 models for detecting various engineering symbols (valves, reducers, flanges, etc.)
- **Instrument Recognition**: Specialized detectors for instrumentation symbols with classification of instrument types
- **Equipment Detection**: Large-scale equipment identification (vessels, heat exchangers, compressors, etc.)
- **Line Detection and Tracing**: Advanced image processing techniques to trace continuous lines and differentiate between process, utility, and instrumentation lines
- **Text Recognition**: OCR pipeline optimized for engineering notation with post-processing for technical abbreviations and identifiers
- **Table Extraction**: Structured data extraction from Heat & Material Balance (H&MB) tables

#### 2. Entity Association:
I implemented sophisticated association algorithms to:

- **Symbol-Text Pairing**: Connect detected symbols with their corresponding labels and identifiers
- **Line Number Association**: Associate line segments with their identifying text using spatial and contextual reasoning
- **Equipment Labeling**: Link equipment with their identification numbers and specifications
- **Hierarchical Grouping**: Group related components into functional units based on spatial proximity and connectivity

#### 3. Graph Construction:
The core of the system involved building a comprehensive process graph:

- **Directed Acyclic Graph (DAG)**: Representation of the entire process flow with components as nodes and connections as edges
- **Topological Analysis**: Identification of process flow direction and critical paths
- **Connectivity Verification**: Validation of graph integrity and detection of disconnected segments
- **Graph Traversal Algorithms**: Custom algorithms for tracing process flows and identifying boundaries

#### 4. Elementary Process Section (EPS) Transfer:
A key innovation was the automated transfer of EPS information:

- **EPS Identification**: Detection of process sections in PFDs with distinct operating conditions
- **Property Extraction**: Automated extraction of temperature, pressure, and composition data from H&MB tables
- **Endpoint Matching**: Advanced algorithm to match EPS endpoints between PFDs and P&IDs
- **Path Optimization**: Identification of the most probable path for EPS propagation using shortest path algorithms
- **Property Propagation**: Transfer of process conditions to all components within each identified EPS

#### 5. QRA Calculation and Visualization:
The final phase involved implementing industry-standard risk assessment:

- **Counting Rules Application**: Implementation of Aramco-specific counting rules for risk assessment
- **Component Classification**: Categorization of components based on risk contribution
- **Risk Calculation**: Automated calculation of failure frequencies and consequence modeling
- **Interactive Dashboard**: Development of a web-based visualization tool with multiple views (symbols, instruments, pipelines, equipment)
- **User Management**: Role-based access control for different stakeholders
- **Export Functionality**: Structured export of QRA results and EPS properties for integration with other systems

## Technical Challenges and Solutions:
The development of this AI-driven QRA system faced several fundamental technical challenges. Vessel symbols varied significantly across different diagram standards and organizations, requiring robust data augmentation techniques.Determining true connectivity in complex diagrams with crossing lines and dense areas was another major challenge that we addressed by developing a multi-pass line tracing algorithm and flow direction indicators. The system also needed to correctly associate text with appropriate components in crowded diagrams, which we solved through a proximity-based association system enhanced with domain-specific rules and contextual analysis.

The system also had to tackle challenges related to process boundaries and scalability. Accurately identifying the boundaries of Elementary Process Sections across different diagram types required implementing a hybrid approach combining topological analysis with process condition discontinuity detection.

## Results and Applications
The AI-driven QRA system achieved remarkable performance metrics, with detection accuracy exceeding 95% for symbols, 92% for instruments, and 98% for major equipment, while maintaining 94% accuracy in text recognition and 90% accuracy in EPS transfer between diagrams. This translated to significant business impact, reducing QRA preparation time by 85% and enabling comprehensive digital transformation through applications like automated risk profiling, rapid change management assessment, digital twin integration, streamlined regulatory compliance, and effective knowledge preservation. The system not only accelerated the analysis process from weeks to hours for complex facilities but also eliminated human variability in interpretation, leading to more consistent and reliable risk assessments while significantly reducing engineering costs and simplifying facility maintenance updates.

## Conclusion:
This project successfully demonstrated the feasibility and advantages of using AI and computer vision to automate the digitization of complex engineering diagrams for quantitative risk analysis. The approach overcomes many limitations of manual methods and provides a foundation for more comprehensive digital transformation in the oil and gas industry.

The combination of advanced object detection, text recognition, and graph-based analysis yielded a robust system capable of handling the complexity and variability of real-world engineering documentation. The technology has been incorporated into Aramco's risk assessment workflow and continues to be developed for broader application across their facilities.

**Further project details and code base are not revealed since the work is under NDA** 