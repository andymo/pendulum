from sim import simulate
import numpy

U = numpy.zeros(1000)
U[0] = 1000

OUTFILE_NAME = "pendulum_sim.csv"

def main():
   data = simulate(U)
   theta = data[0]
   theta_dot = data[1]
   x = data[2]
   x_dot = data[3]

   #because our version of savetxt doesn't have the header option for some reason
   with open(OUTFILE_NAME, 'w') as f:
      f.write("theta,theta_dot,x,x_dot,u\n")
      f.write("float,float,float,float,float\n")
      f.write(",,,,\n")
      numpy.savetxt(f, (data,U), delimiter=',', fmt="%.18f")
   

if __name__ == "__main__":
   main()
