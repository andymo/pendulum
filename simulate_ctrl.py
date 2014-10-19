#!/usr/bin/env python
from sim import simulate, ctrl_simulate, plot_traj
from math import pi
import numpy as np

X0 = [pi, 0.1, 0, 0]

OUTFILE_NAME = "ctrl_sim.csv"

def main():
   data, U, _t = ctrl_simulate(X0, 1000)
   theta = data[0]
   theta_dot = data[1]

   #get all of our theta within -pi:pi
   i = len(data[0]) - 1

   while i > -1:
      while not -pi <= data[0][i] <= pi:
         if data[0][i] < -pi:
            data[0][i] = data[0][i] + 2*pi
         else:
            data[0][i] = data[0][i] - 2*pi
      i = i - 1

   #because our version of savetxt doesn't have the header option for some reason
   with open(OUTFILE_NAME, 'w') as f:
      f.write("theta,theta_dot,u\n")
      f.write("float,float,float\n")
      f.write(",,\n")
      trimmed_data = data[:2]
      trimmed_data = np.vstack([trimmed_data, U])
      np.savetxt(f, np.transpose(trimmed_data), delimiter=',', fmt="%.18f")

   plot_traj(data, U, _t)

   

if __name__ == "__main__":
   main()

