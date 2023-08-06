#!/usr/bin/env python3
import numpy as np
import os, sys
sys.path.append(os.getcwd())
from FisInMa import *


def baranyi_roberts_ode(t, x, u, p, ode_args):
    x1, x2 = x
    Temp, = u
    x_max, b, Temp_min = p
    mu_max = b**2 * (Temp - Temp_min)**2
    return [
        mu_max * (x2/(x2 + 1)) * (1 - x1/x_max) * x1,
        mu_max * x2
    ]

def ode_dfdp(t, x, u, p, ode_args):
    x1, x2 = x
    Temp, = u
    x_max, b, Temp_min = p
    mu_max = b**2 * (Temp - Temp_min)**2
    return [
        [
            mu_max*(x2/(x2 + 1))*(x1/x_max)**2,
             2*b*(Temp - Temp_min)**2*(x2/(x2 + 1))
                *(1 - x1/x_max)*x1,
            -2*b**2 * (Temp - Temp_min)*(x2/(x2 + 1))
                *(1 - x1/x_max)*x1
        ],
        [
            0,
            2*b*(Temp - Temp_min)**2*x2,
            2*b**2*(Temp - Temp_min)*x2
        ]
    ]

def ode_dfdx(t, x, u, p, ode_args):
    x1, x2 = x
    Temp, = u
    x_max, b, Temp_min = p
    mu_max = b**2 * (Temp - Temp_min)**2
    return [
        [
            mu_max * (x2/(x2 + 1)) * (1 - 2*x1/x_max),
            mu_max * 1/(x2 + 1)**2 * (1 - x1/x_max)*x1
        ],
        [
            0,                                                  # df2/dx1
            mu_max                                              # df2/dx2
        ]
    ]


if __name__ == "__main__":
    # Define parameters and initial conditions
    p = (1e8, 0.2, 1.0) # (x_max, b, T_min)
    x0 = np.array([1e3, 0.1]) 

    # Define interval and number of sampling points for times
    times = {"lb": 0.0, "ub": 10.0, "n": 6}

    # Define explicit temperature points
    Temp_low = 8.0
    Temp_high = 10.0
    n_Temp = 1

    # Summarize all input definitions in list (only temperatures)
    inputs = [
        np.linspace(Temp_low, Temp_high, n_Temp)
    ]

    # Create the FisherModel which serves as the entry point
    #  for the solving and optimization algorithms
    fsm = FisherModel(
        ode_x0=x0,
        ode_t0=0.0,
        ode_fun=baranyi_roberts_ode,
        ode_dfdx=ode_dfdx,
        ode_dfdp=ode_dfdp,
        ode_initial=x0,
        times=times,
        inputs=inputs,
        parameters=p,
        obs_fun=0,
        covariance={"abs": 0.3, "rel": 0.1}
    )

    fsr = find_optimal(
        fsm,
        relative_sensitivities=True,
        recombination=0.7,
        mutation=(0.1, 0.8),
        workers=-1,
        popsize=10,
        polish=False,
    )

    # Plot all ODE results with chosen time points
    # for different data points
    plot_all_solutions(fsr)
    json_dump(fsr, "baranyi_roberts.json")
