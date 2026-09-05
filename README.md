# Planar Swarm Consensus Simulation

A Python simulation of a decentralized multi-agent swarm using
graph-based communication and consensus control.

The project models a swarm of autonomous agents whose communication
network is represented as a graph. Each agent uses information from its
neighbors to coordinate its motion, demonstrating how local interactions
can produce coordinated behavior across the swarm.

The simulation currently uses simplified 2D agent dynamics and supports
large swarms with configurable communication topologies.

## Demo


## Overview

Multi-agent systems can be represented using graph theory:

- **Nodes** represent individual drones.
- **Edges** represent communication between drones.
- The **graph Laplacian** represents the connectivity of the swarm.
- A **consensus controller** uses information from neighboring agents to
  coordinate their behavior.

This project combines graph theory, dynamical systems, and control theory
to simulate decentralized swarm behavior.

### Agent State

Each drone is represented by a four-dimensional state:

$$
x_i =
\begin{bmatrix}
x_i & y_i & v_{x,i} & v_{y,i}
\end{bmatrix}^T
$$

where $x$ and $y$ represent position and $v_x$ and $v_y$ represent velocity.

## Project Structure

```text
drone-swarm/
│
├── drone_swarm/
│   ├── drone_swarm_controller.py
│   ├── drone_swarm_dynamics.py
│   ├── drone_swarm_param.py
│   ├── drone_swarm_plotter.py
│   ├── drone_swarm_sim.py
│   └── test_plotter.py
│
├── LICENSE
├── README.md
└── .gitignore