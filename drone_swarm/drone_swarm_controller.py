import numpy as np
from scipy.linalg import solve_continuous_are

class SwarmController:
    def __init__(self, Param, Initial_state):
        self.A = Param["A"]
        self.B = Param["B"]
        self.L = Param["L"].toarray().astype(float)
        
        self.agents = len(Initial_state[:,0])
        self.State = Initial_state
        self.num_states = Param["num_states"]
        self.num_inputs = Param["num_inputs"]
        self.Input = np.zeros((self.agents, self.num_inputs))
        
        self.Q = Param["Q"]
        self.R = Param["R"]
        
        self.u_min = Param["u_min"]
        self.u_max = Param["u_max"]
        
        self.friction = Param["mu"]*Param["m"]*Param["g"]
        self.k_frict = Param["k_frict"]
        
        self.K = self.calculate_gains()
        
    def update(self, state):
        # reshape state into a vector for control law
        self.state = np.reshape(state, (self.agents*self.num_states, 1))
        
        # calculate control input using consensus
        kron_prod = np.kron(self.L, self.K)
        u_tilde = -kron_prod @ self.state
        
        # saturate input
        u_sat = self.saturate(u_tilde)
        
        # feedback linearization (adding friction back to the input)
        V = np.reshape(state[:, 2:4], (self.agents*2, 1))
        F = self.friction * np.tanh(self.k_frict * V)
        self.input = u_sat + F
        
        return self.input
    
    def calculate_gains(self):
        # check controllability
        self.kalman_controllability()
        
        # solve the algebraic riccotti equation for P
        P = solve_continuous_are(self.A, self.B, self.Q, self.R)
        
        # extract optimal gains matrix
        R_inv = np.linalg.inv(self.R)
        K = R_inv @ self.B.T @ P
        
        return K
        
    def kalman_controllability(self):
        # initialize controllability matrix
        n = self.A.shape[1]
        m = self.B.shape[1]
        C_AB = np.zeros((n,m*n))
        
        # populate matrix
        for i in range(0,n):
            start_col = i*m
            end_col   = i*m + m
            C_AB[:, start_col:end_col] = np.linalg.matrix_power(self.A, i) @ self.B
            
        # check rank of controllability matrix
        rank = np.linalg.matrix_rank(C_AB)
        if rank == n: 
            pass
        else:
            raise ValueError(f"system is partially controllable. rank: {rank}")
        
    def saturate(self, u):
        """Saturate input"""
        return np.clip(u, self.u_min, self.u_max)
          