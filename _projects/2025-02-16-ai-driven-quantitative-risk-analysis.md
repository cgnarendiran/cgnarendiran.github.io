---
layout: project
title:  AI-Driven Quantitative Risk Analysis
date:   2025-02-16
image:  images/project12/cover.png
tags:   QRA P&ID PFD digitization computer-vision deep-learning oil-gas Aramco graph-algorithms
---
*On the cover: Digitized Piping and Instrumentation Diagram (P&ID) with highlighted Elementary Process Sections (EPS)*

This work was conducted at Saudi Aramco. The project aimed to develop an automated system for digitizing Process Flow Diagrams (PFDs) and Piping and Instrumentation Diagrams (P&IDs) to enable efficient and accurate Quantitative Risk Analysis (QRA).

## Background:
In the oil and gas industry, Quantitative Risk Analysis is crucial for ensuring operational safety and regulatory compliance. Traditionally, this process involves manual interpretation of complex engineering diagrams such as P&IDs and PFDs, which is time-consuming, error-prone, and requires specialized expertise. These diagrams contain critical information about process equipment, instrumentation, and piping systems that form the basis for risk assessment.

The challenges with traditional manual approaches include:
- Inconsistent interpretation across different engineers
- Time-intensive process (weeks to months for large facilities)
- Difficulty in maintaining up-to-date risk assessments as facilities evolve
- Limited traceability between risk calculations and source documentation

Automating this process through AI and computer vision offers significant advantages in terms of speed, consistency, and accuracy, ultimately enhancing facility safety and operational efficiency.

## Methodology:
The AutoQRA project was structured in five main phases:

### 1. Document Detection and Recognition:
I developed a comprehensive detection system that included:

- **Multi-scale Object Detection**: Custom-trained YOLOv5 models for detecting various engineering symbols (valves, reducers, flanges, etc.)
- **Instrument Recognition**: Specialized detectors for instrumentation symbols with classification of instrument types
- **Equipment Detection**: Large-scale equipment identification (vessels, heat exchangers, compressors, etc.)
- **Line Detection and Tracing**: Advanced image processing techniques to trace continuous lines and differentiate between process, utility, and instrumentation lines
- **Text Recognition**: OCR pipeline optimized for engineering notation with post-processing for technical abbreviations and identifiers
- **Table Extraction**: Structured data extraction from Heat & Material Balance (H&MB) tables

### 2. Entity Association:
I implemented sophisticated association algorithms to:

- **Symbol-Text Pairing**: Connect detected symbols with their corresponding labels and identifiers
- **Line Number Association**: Associate line segments with their identifying text using spatial and contextual reasoning
- **Equipment Labeling**: Link equipment with their identification numbers and specifications
- **Hierarchical Grouping**: Group related components into functional units based on spatial proximity and connectivity

### 3. Graph Construction:
The core of the system involved building a comprehensive process graph:

- **Directed Acyclic Graph (DAG)**: Representation of the entire process flow with components as nodes and connections as edges
- **Topological Analysis**: Identification of process flow direction and critical paths
- **Connectivity Verification**: Validation of graph integrity and detection of disconnected segments
- **Graph Traversal Algorithms**: Custom algorithms for tracing process flows and identifying boundaries

### 4. Elementary Process Section (EPS) Transfer:
A key innovation was the automated transfer of EPS information:

- **EPS Identification**: Detection of process sections in PFDs with distinct operating conditions
- **Property Extraction**: Automated extraction of temperature, pressure, and composition data from H&MB tables
- **Endpoint Matching**: Advanced algorithm to match EPS endpoints between PFDs and P&IDs
- **Path Optimization**: Identification of the most probable path for EPS propagation using shortest path algorithms
- **Property Propagation**: Transfer of process conditions to all components within each identified EPS

### 5. QRA Calculation and Visualization:
The final phase involved implementing industry-standard risk assessment:

- **Counting Rules Application**: Implementation of Aramco-specific counting rules for risk assessment
- **Component Classification**: Categorization of components based on risk contribution
- **Risk Calculation**: Automated calculation of failure frequencies and consequence modeling
- **Interactive Dashboard**: Development of a web-based visualization tool with multiple views (symbols, instruments, pipelines, equipment)
- **User Management**: Role-based access control for different stakeholders
- **Export Functionality**: Structured export of QRA results and EPS properties for integration with other systems

## Technical Challenges and Solutions:

### 1. Symbol Variability:
**Challenge**: Engineering symbols vary across different diagram standards and even within the same organization.
**Solution**: Implemented data augmentation techniques and developed a symbol normalization pipeline that could handle variations in scale, orientation, and style.

### 2. Line Connectivity:
**Challenge**: Determining true connectivity in complex diagrams with crossing lines and dense areas.
**Solution**: Developed a multi-pass line tracing algorithm that utilized junction analysis and flow direction indicators to resolve ambiguities.

### 3. Text Association:
**Challenge**: Correctly associating text with the appropriate components in crowded diagrams.
**Solution**: Created a proximity-based association system enhanced with domain-specific rules and contextual analysis.

### 4. EPS Boundary Detection:
**Challenge**: Accurately identifying the boundaries of Elementary Process Sections across different diagram types.
**Solution**: Implemented a hybrid approach combining topological analysis with process condition discontinuity detection.

### 5. Scalability:
**Challenge**: Processing large-scale facility diagrams with thousands of components.
**Solution**: Developed a tiling approach that processed diagram sections in parallel while maintaining global connectivity information.

## Results:
The AI-driven QRA system demonstrated significant improvements over traditional manual methods:

### Performance Metrics:
- **Detection Accuracy**: >95% for symbols, >92% for instruments, >98% for major equipment
- **Text Recognition**: >94% accuracy for engineering notation and identifiers
- **EPS Transfer Accuracy**: >90% correct mapping between PFDs and P&IDs
- **Processing Time**: Reduced analysis time from weeks to hours for complex facilities
- **Consistency**: Eliminated human variability in interpretation

### Business Impact:
- **Efficiency Gain**: 85% reduction in time required for QRA preparation
- **Cost Savings**: Significant reduction in engineering hours required for risk assessment
- **Quality Improvement**: More comprehensive and consistent risk analysis
- **Maintenance Simplification**: Easier updates when facility modifications occur
- **Knowledge Capture**: Digitized representation of facility knowledge previously locked in paper documents

## Applications:
The developed technology enables several applications in the oil and gas industry:

1. **Quantitative Risk Assessment**: Automated calculation of risk profiles for facilities
2. **Change Management**: Rapid assessment of safety implications for proposed facility modifications
3. **Digital Twin Integration**: Foundation for comprehensive digital representation of physical assets
4. **Regulatory Compliance**: Streamlined documentation for safety case submissions
5. **Knowledge Transfer**: Preservation of facility design knowledge in accessible digital format

## Conclusion:
This project successfully demonstrated the feasibility and advantages of using AI and computer vision to automate the digitization of complex engineering diagrams for quantitative risk analysis. The approach overcomes many limitations of manual methods and provides a foundation for more comprehensive digital transformation in the oil and gas industry.

The combination of advanced object detection, text recognition, and graph-based analysis yielded a robust system capable of handling the complexity and variability of real-world engineering documentation. The technology has been incorporated into Aramco's risk assessment workflow and continues to be developed for broader application across their facilities.

**Further project details and code base are not revealed since the work is under NDA** 