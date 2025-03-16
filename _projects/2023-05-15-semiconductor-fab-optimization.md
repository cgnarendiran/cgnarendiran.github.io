---
layout: project
title:  Semiconductor Fab Optimization using Reinforcement Learning
date:   2023-05-15
image:  images/project11/cover.jpeg
tags:   reinforcement-learning semiconductor manufacturing optimization RL dashboard
---
*On the cover: Visualization of wafer lots in a semiconductor fab*

This project focused on developing and implementing a Reinforcement Learning (RL) solution to optimize semiconductor fabrication operations using the SMT2020 fab testbed. The primary goal was to reduce queue lengths and improve cycle times without sacrificing throughput or yield.

## Background:
Semiconductor fabrication is one of the most complex manufacturing processes, involving hundreds of steps, expensive equipment, and strict quality requirements. Traditional scheduling approaches like dispatching rules (FIFO, EDD, CR) or optimization-based methods struggle to handle the dynamic and stochastic nature of semiconductor manufacturing. Reinforcement Learning offers a promising alternative by learning optimal policies through interaction with the environment.

The challenges in semiconductor manufacturing include:
- Long cycle times (often 8-12 weeks from start to finish)
- Complex routing with re-entrant flows
- Expensive equipment with high utilization requirements
- Frequent maintenance and unexpected downtimes
- Varying product mixes and priorities

## Methodology:
The project implemented a custom RL agent to make setup switching decisions across the fab:

- **State Space**: Included queue lengths at each tool group, WIP distribution, tool availability, lot priorities, and estimated processing times
- **Action Space**: Decisions on which lot to process next and when to perform setup changes on tools
- **Reward Function**: Primarily focused on minimizing queue lengths while balancing throughput and cycle time objectives

The agent was trained using Proximal Policy Optimization (PPO) with curriculum learning and experience replay to efficiently learn from past experiences. The training process gradually increased complexity, starting with simpler scenarios and moving to more realistic fab conditions.

## Results:
The RL-based setup switching agent achieved remarkable improvements:

- **50% reduction in average queue lengths** across critical tool groups
- **32% improvement in cycle time** for high-priority products
- **18% increase in overall fab throughput**
- **27% reduction in setup-related downtime**

These significant improvements attracted new customers to the fab, as the reduced cycle times and increased throughput provided a competitive advantage in the market.

![dashboard](/images/project13/dashboard.png)
*Interactive dashboard showing KPI comparisons between different scheduling policies*

A key component of the project was the development of an interactive panel-based dashboard that enabled:

- Side-by-side comparison of different scheduling policies (RL agent vs. traditional methods)
- Real-time monitoring of critical KPIs including queue lengths, cycle times, and throughput
- Interactive Gantt charts showing tool utilization and lot processing
- Visualization of agent learning progress including reward curves and policy metrics

The dashboard became an essential tool for operations managers to understand the benefits of the RL approach and make informed decisions about policy deployment.

## Technical Implementation:
The solution was implemented using Python for the core RL algorithms, PyTorch for neural network implementation, Ray/RLlib for distributed training, and Panel/Holoviz for the interactive dashboard.

Several challenges were encountered during the project, including the high-dimensional state space, sparse rewards, and long-horizon dependencies typical in semiconductor manufacturing. These were addressed through feature engineering, reward shaping, and hierarchical RL approaches.

The project demonstrated the significant potential of Reinforcement Learning for semiconductor fabrication optimization, providing a compelling business case for the adoption of AI-driven scheduling in semiconductor manufacturing.
