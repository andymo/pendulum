from scipy.integrate import odeint
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt

def sys(x, t):
    M = 0.5     # [kg] mass of the cart
    m = 0.2     # [kg] mass of the pendulum
    l = 0.3     # [m] length from pendulum center to cart
    g = -9.81

    u = x[4]

    x_0_dot = x[1]
    x_1_dot = (( u*cos(x[0]) - (M+m)*g*sin(x[0]) + m*l*(cos(x[0])*sin(x[0]))*pow(x[1],2) ) /
                ( m*l*pow(cos(x[0]),2) - (M+m)*l ))
    x_2_dot = x[3]
    x_3_dot = (( u + m*l*sin(x[0])*pow(x[1],2) - m*g*cos(x[0])*sin(x[0]) ) /
                ( M + m - m*pow(cos(x[0]),2) ))
    return np.asarray([x_0_dot, x_1_dot, x_2_dot, x_3_dot, 0])

def next_step(x, u, t):
    dt = 0.1
    t = np.linspace(t, t+dt, 2)
    # print x.append(u)
    x_next = odeint(sys, np.append(x,u), t)
    return x_next[1,0:4], t[1]

def simulate(x0, U):
    T = np.zeros(len(U))
    X = np.zeros((len(x0), len(U)))
    X[:,0] = x0
    for i in np.asarray(range(len(U)-1)):
        x,t = next_step(X[:,i], U[i], T[i])
        #print x
        #print t
        X[:,i+1] = x
        T[i+1] = t
    return X, T

def plot_traj(X, U, T):
    plt.subplot(511)
    plt.plot(T, X[0,:], 'b')
    plt.ylabel("Theta")

    plt.subplot(512)
    plt.plot(T, X[1,:], 'b')
    plt.ylabel("Angular Velocity")
    
    plt.subplot(513)
    plt.plot(T, X[2,:], 'b')
    plt.ylabel("Position")

    plt.subplot(514)
    plt.plot(T, X[3,:], 'b')
    plt.ylabel("Velocity")
    
    plt.subplot(515)
    plt.plot(T, U, 'k')
    plt.ylabel("Control")

    plt.show()

