import matplotlib.pyplot as plt
import numpy as np


class SwarmPlotter:

    def __init__(self, State, target_agent_idx=0):
        self.state = State
        self.num_agents = len(self.state[:, 0]) // 4
        self.target_idx = target_agent_idx

        # History buffer to track position over time for the target agent
        self.target_history_x = [self.state[self.target_idx, 0]]
        self.target_history_y = [self.state[self.target_idx, 1]]

        # Turn on interactive mode for real-time plotting
        plt.ion()

        # Set up a 1x2 grid: Left for Swarm Scatter, Right for Single-Agent Trajectory
        self.fig, (self.ax_swarm, self.ax_trace) = plt.subplots(
            1, 2, figsize=(12, 5)
        )

        # 1. Setup Swarm Scatter Plot
        self.ax_swarm.set_title("Real-Time Swarm Convergence")
        self.ax_swarm.set_xlabel("X Position")
        self.ax_swarm.set_ylabel("Y Position")
        self.ax_swarm.grid(True)

        x_pos = self.state[:, 0]
        y_pos = self.state[:, 1]
        self.scatter = self.ax_swarm.scatter(
            x_pos, y_pos, color="blue", edgecolors="k", zorder=3
        )

        # Highlight the tracked agent in red
        self.target_scatter = self.ax_swarm.scatter(
            x_pos[self.target_idx],
            y_pos[self.target_idx],
            color="red",
            s=80,
            zorder=4,
            label=f"Agent {self.target_idx}",
        )
        self.ax_swarm.legend(loc="upper right")

        # Limits for the swarm view
        self.ax_swarm.set_xlim(x_pos.min() - 5, x_pos.max() + 5)
        self.ax_swarm.set_ylim(y_pos.min() - 5, y_pos.max() + 5)

        # 2. Setup Position vs. Time Plot
        self.ax_trace.set_title(f"Agent {self.target_idx} Position vs. Time")
        self.ax_trace.set_xlabel("Time Step")
        self.ax_trace.set_ylabel("Position")
        self.ax_trace.grid(True)

        (self.line_x,) = self.ax_trace.plot([], [], "r-", label="X Position")
        (self.line_y,) = self.ax_trace.plot([], [], "b-", label="Y Position")
        self.ax_trace.legend(loc="upper right")

    def update_frame(self, state):
        """Updates both the swarm scatter plot and the single-agent trajectory plot."""
        self.state = state
        positions = self.state[:, 0:2]

        # 1. Update overall swarm positions
        self.scatter.set_offsets(positions)

        # Update highlighted target agent marker position
        target_pos = positions[self.target_idx : self.target_idx + 1]
        self.target_scatter.set_offsets(target_pos)

        # 2. Record target agent position history
        self.target_history_x.append(target_pos[0, 0])
        self.target_history_y.append(target_pos[0, 1])

        # 3. Update line plot data
        steps = np.arange(len(self.target_history_x))
        self.line_x.set_data(steps, self.target_history_x)
        self.line_y.set_data(steps, self.target_history_y)

        # Rescale the time plot axes dynamically as history grows
        self.ax_trace.relim()
        self.ax_trace.autoscale_view()

        # 4. Flush graphics to screen
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()