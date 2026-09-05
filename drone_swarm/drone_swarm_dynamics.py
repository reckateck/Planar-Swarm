# this class represents the dynamics for a swarm of planar double integrator robots. for simulation 
# stability friction is modeled as a damper where friction force is divided by a nominal velocity to 
# create a damping coefficient.  

import numpy as np

class SwarmDynamics:
    def __init__(self, initial_state, frequency, Param):
        self.agents = len(initial_state[:,0])
        self.State = initial_state
        self.num_states = Param["num_states"]
        self.num_inputs = Param["num_inputs"]
        self.Input = np.zeros((self.agents, self.num_inputs))
        self.dt = 1/frequency
        
        # define physics parameters
        self.m       = Param["m"] # kg
        self.mu      = Param["mu"] # friction coeff [unitless]
        self.g       = Param["g"] # m/s^2
        self.k_frict = Param["k_frict"]
        
    def update(self, State, Input):
        """update dynamics forward one time step into the future"""
        # update dynamic variables
        self.State = np.reshape(State, (self.agents, self.num_states))
        self.Input = np.reshape(Input, (self.agents, self.num_inputs))
        
        # predict future state (numerical integration)
        self.rk4()
        
        return self.State
        
    def rk4(self):
        """Use Time Invariant Runge-Kutta 4 to numerically integrate the state forward one timestep"""
        # calculate derivative slopes
        k1 = self.states_dot(statestep = 0)
        k2 = self.states_dot(statestep=k1*self.dt/2.0)
        k3 = self.states_dot(statestep=k2*self.dt/2.0)
        k4 = self.states_dot(statestep=k3*self.dt)
        
        # update state
        self.State = self.State + self.dt/6.0 * (k1 + 2*k2 + 2*k3 + k4)
        
    def states_dot(self, statestep):
        """Calcluate current timestep's state derivative for numerical integration"""
        # reshape global state vector into matrix (# of agents x # of local states) for vectorized computation
        X = self.State + statestep
        U = self.Input
        
        # calculate regularized coulomb friction to remove RK$ chatter
        V = X[:,2:4]
        F_friction = -self.mu*self.m*self.g * np.tanh(self.k_frict * V)
        
        # calculate state derivative matrix
        X_dot = np.zeros((self.agents, self.num_states))
        X_dot[:,0:2] = X[:,2:4]
        X_dot[:,2:4] = (U[:,0:2] + F_friction) / self.m
        
        return X_dot
    
    def states_dot_ss(self, State, Input):
            """Calcluate the state derivative"""
            # reshape global state vector into matrix (# of agents x # of local states) for vectorized computation
            X = State 
            U = Input
            
            # calculate coulomb friction
            V = X[:,2:4]
            F_friction = -self.mu*self.m*self.g * np.sign(V)
            
            # calculate state derivative matrix
            X_dot = np.zeros((self.agents, self.num_states))
            X_dot[:,0:2] = X[:,2:4]
            X_dot[:,2:4] = (U[:,0:2] + F_friction) / self.m
            
            return X_dot
        