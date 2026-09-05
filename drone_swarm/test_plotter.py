import numpy as np
import matplotlib.pyplot as plt
from drone_swarm_plotter import SwarmPlotter
import time

# initialization
x_i = np.array([[1.0], [1.0], [0], [0], [0], [1.0], [0], [0], [1.0], [0], [0], [0], [-1.0], [-1.0], [0], [0]])
plotter = SwarmPlotter(x_i)

for i in range(1,20,1):
    x_i += np.array([[0.1], [0.1], [0], [0], [0], [0.1], [0], [0], [0.1], [0], [0], [0], [-0.1], [-0.1], [0], [0]])
    plotter.update_frame(x_i)
    time.sleep(1)