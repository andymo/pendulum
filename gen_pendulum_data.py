#!/usr/bin/env python
from sim import simulate
import numpy
from math import pi
from random import *

def random_walk(n):
    x = [gauss(0,0.01)]
    for step in range(n-1):
        x.append(x[-1] + gauss(0,0.01))
    return x

U = random_walk(1000)
X0 = [.75*pi, 0, 0, 0]

OUTFILE_NAME = "pendulum_sim.csv"

def main():
   data, _t = simulate(X0,U)
   theta = data[0]
   theta_dot = data[1]
   x = data[2]
   x_dot = data[3]
   data = numpy.vstack([data, U])

   #get all of our theta within -pi:pi
   i = len(data[0]) - 1

   while i > -1:
      while not -pi < data[0][i] < pi:
         if data[0][i] < -pi:
            data[0][i] = data[0][i] + 2*pi
         else:
            data[0][i] = data[0][i] - 2*pi
      i = i - 1

   #because our version of savetxt doesn't have the header option for some reason
   with open(OUTFILE_NAME, 'w') as f:
      f.write("theta,theta_dot,x,x_dot,u\n")
      f.write("float,float,float,float,float\n")
      f.write(",,,,\n")
      numpy.savetxt(f, numpy.transpose(data), delimiter=',', fmt="%.18f")
   

if __name__ == "__main__":
   main()