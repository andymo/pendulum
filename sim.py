from scipy.integrate import odeint
from scipy.linalg import solve_continuous_are
from numpy.linalg import inv
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt

M        = 0.5     # [kg]      mass of the cart
m        = 0.2     # [kg]      mass of the pendulum
l        = 0.3     # [m]       length from pendulum center to cart
I        = 0.006   # [kg*m^2]  moment of inertia
gravity  = 9.81    # [m/(s^2)] acceleration from gravityravity
friction = 0.1     # [N/m/sec] coefficient of friction of cart
a        = 0.1     # [N/r/sec] coefficient of friction of pendulum

m_l    = m*l
m2_l2  = m_l*m_l  #m2_l2 for readability?
m3_l3  = m2_l2*m_l
M_m    = M + m
I_p    = I + m_l*l

denom  = ( I * M_m ) + ( M * m_l * l )

A22  = -I_p     * friction      / denom
A23  =  gravity * m2_l2         / denom
A42  = -m_l     * friction      / denom
A43  =  m_l     * gravity * M_m / denom
A44  =  a                       / denom

B2   = I_p                      / denom
B4   = m_l                      / denom

A = np.asarray([
    [ 0,    1,      0,      0   ],
    [ 0,    A22,    A23,    0   ],
    [ 0,    0,      0,      1   ],
    [ 0,    A42,    A43,    A44 ] ])

B = np.asarray([[0], [B2], [0], [B4]])

Q = np.asarray([
    [ 10,   0,  0,  0 ],
    [ 0,    1,  0,  0 ],
    [ 0,    0,  0,  0 ],
    [ 0,    0,  0,  0 ] ])


R = np.asarray([[0.1]])

P = solve_continuous_are(A, B, Q, R)

derp = np.dot(1/R, np.transpose(B))
print derp
K = np.dot(derp, P)
print K

def control(state):
    ref = np.asarray([np.pi,0,0,0])
    print ref
    print state
    return -np.dot(K, state-ref)


def sys(state, t):
    theta       = state[0]
    theta_dot   = state[1]
    s_dot       = state[3]
    u           = state[4]

    cos_theta        = cos(theta)
    sin_theta        = sin(theta)
    cos2_theta       = cos_theta*cos_theta
    sin2_theta       = sin_theta*sin_theta
    cossin_theta     = sin_theta*cos_theta
    theta_dot2       = theta_dot*theta_dot
    m2_l2_cos2_theta = m2_l2*cos2_theta


    s_ddot      = (( I_p * u 
                   + I_p * m_l * theta_dot2 * sin_theta
                   + gravity * m2_l2 * cossin_theta
                   - I_p * friction * s_dot )
                  / ( I_p * M_m
                  + m2_l2_cos2_theta ))


    theta_ddot  = ((( m_l * cos_theta * u 
                    + m2_l2 * cossin_theta * theta_dot2
                    - m_l * cos_theta * friction * s_dot 
                    + ( gravity * m3_l3 * cossin_theta * cos_theta / I_p ))
                  / ( I_p * M_m + m2_l2_cos2_theta ))
                - ( ( m_l * gravity * sin_theta + a * theta_dot ) 
                  / I_p ))



    return np.asarray([theta_dot, theta_ddot, s_dot, s_ddot, 0])

def next_step(x, u, t):
    dt = 0.05
    t = np.linspace(t, t+dt, 2)
    # print x.append(u)
    x_next = odeint(sys, np.append(x,u), t)
    return x_next[1,0:4], t[1]

def ctrl_simulate(x0, num_times_steps):
    T = np.zeros(num_times_steps) 
    X = np.zeros((len(x0), num_times_steps))
    U = np.zeros(num_times_steps)
    X[:,0] = x0
    for i in np.asarray(range(num_times_steps-1)):
        U[i] = control(X[:,i])
        X[:,i+1], T[i+1] = next_step(X[:,i], control(X[:,i]), T[i])
    return X, U, T

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

