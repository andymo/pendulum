# Inverted Pendulum Prediction

The program in this folder is designed to predict the position (angle) of an inverted pendulum mounted on a cart along a track. Heavily based off of NuPIC's "One Hot Gym Prediction" tutorial.

## Premise

This doesn't work.

This is because the system is time-invariant; the next state is determined 100% based upon the current state and not the history of all states. Because of this lack of dependence on context, the temporal pooler is effectively unnecessary.

We knew that there are already existing machines to handle balancing an inverted pendulum ([LQRs](http://en.wikipedia.org/wiki/Linear-quadratic_regulator)), but our purpose here was to determine whether or not NuPIC would be able to do it in some form as well.

Philosophically, there is no such thing as time-series data. The emergence of time series are a testament to the fact that you can't actually see all states at once, so the history of a given state can be used to determine the state of the rest of the system (in order to calculate the next state).

## Program Description

This is a program consisting of a simple collection of Python scripts using NuPIC's [Online Prediction Framework](https://github.com/numenta/nupic/wiki/Online-Prediction-Framework). Program execution is described in the [Running the Program](#running-the-program) section below. There are two steps this program performs to get predictions for the input data from the [pendulum_sim.csv](pendulum_sim.csv) file, which are described below. There is also an optional step ([Cleanup](#cleanup)), which removes artifacts from the files system after the previous steps have run.

## Program Phases

### 1. Swarming Over the Input Data

Swarming ain't perfect, but it is an essential way for us to find the best NuPIC model parameters for a particular data set. It only needs to be done once, and can be performed over a subset of the data. NuPIC knows nothing about the structure and data types within [pendulum_sim.csv](pendulum_sim.csv), so we have to define this data.

## Running the Program

This program consists of 3 Python scripts you can execute from the command line and a few helper modules. The executable scripts are `swarm.py`, `run.py`, and `cleanup.py`. Each script prints out a description of the actions it takes when executed.

### Generating Pendulum Simulation Data

   ./gen_pendulum_data.py

[gen_pendulum_data.py](gen_pendulum_data.py) runs the simulation in sim.py with random forces applied to the cart every so often. This generates [pendulum_sim.csv](pendulum_sim.csv) with pendulum positional data (theta, theta_dot (angular velocity), x, x_dot (cart positional velocity), and u (the force applied to the cart)).

### Swarming

    ./swarm.py

Hard-coded to run the [pendulum_sim.csv](pendulum_sim.csv). 

### Running

    ./run.py [--plot]

If `--plot` is not specified, writes predictions to `pendulum_sim_out.csv` file within the current working directory. If `--plot` is specified, will attempt to plot on screen using **matplotlib**. If matplotlib is not installed, this will fail miserably.

### Cleanup

    ./cleanup.py

The previous steps leave some artifacts on your file system. Run this command to clean them up and start from scratch.
