import numpy as np

Param = {}

### 
### Plant Parameters ###
Param["m"]       = 1.0  # kg
Param["mu"]      = 0.3  # friction coeff [unitless]
Param["g"]       = 9.81 # m/s^2
Param["k_frict"] = 50.0 # numerical stability coefficient [unitless]

### Graph parameters ###


### State Space Parameters ###
Param["A"] = np.array([[0, 0, 1.0, 0], [0, 0, 0, 1.0], [0, 0, 0, 0], [0, 0, 0, 0]])
Param["B"] = np.array([[0, 0], [0, 0], [1/Param["m"], 0], [0, 1/Param["m"]]])

Param["num_states"] = Param["A"].shape[1]
Param["num_inputs"] = Param["B"].shape[1]

### Controller Parameters ###
Param["Q"] = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]])
Param["R"] = 1.0 * np.eye(2)

Param["u_min"] = -10
Param["u_max"] = 10