import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import time
from drone_swarm_plotter import SwarmPlotter
from drone_swarm_dynamics import SwarmDynamics
from drone_swarm_param import Param
from drone_swarm_controller import SwarmController

### Global Simulation Parameters ###
SIM_LENGTH = 15 # seconds
SIM_FREQUENCY = 60 # hertz
PLOT_FREQUENCY = 10 # hertz
TOTAL_STEPS = int(SIM_LENGTH*SIM_FREQUENCY)
STEPS_PER_PLOT = int(SIM_FREQUENCY/PLOT_FREQUENCY)
AGENTS = 100
RAD = 0.25

# Generate the graph
G = nx.random_geometric_graph(n=AGENTS, radius=RAD, dim=2)

# laplacian matrix of the graph
Param["L"] = nx.laplacian_matrix(G)

# Extract positions and convert dictionary values to a NumPy array
pos_dict = nx.get_node_attributes(G, "pos")
pos = np.array(list(pos_dict.values())) * 100  # Scale up from unit square

# Define global initial state: shape (N, 4) -> [x, y, vx, vy]
INITIAL_STATE = np.zeros((len(pos), 4))
INITIAL_STATE[:, 0:2] = pos
INITIAL_STATE[:, 2:4] = np.ones_like(pos)

### main simulation loop ###
# instantiate classes and initialize states
plotter = SwarmPlotter(INITIAL_STATE)
dynamics = SwarmDynamics(INITIAL_STATE, SIM_FREQUENCY, Param)
controller = SwarmController(Param, INITIAL_STATE)

start_time = time.perf_counter()
for n in range(TOTAL_STEPS):
    # figure out state (i'm assuming perfect sensors so the state is pulled directly from dynamics)
    t = n * 1/SIM_FREQUENCY
    State = dynamics.State
    
    # determine control input
    u = controller.update(State)
    
    # calculate state 
    next_state = dynamics.update(State=State,Input=u)
    
    # Plot and animate system
    if n % STEPS_PER_PLOT == 0:
        plotter.update_frame(state=next_state)
        plt.pause(0.001)

    
### Display Simulation Metrics ###
print(f"Simulation took {time.perf_counter() - start_time} seconds")