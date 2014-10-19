#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is derived from component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

import nupic_output

import numpy as np
from sim import next_step, control
from math import pi


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the pendulum into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
PENDULUM_NAME = "pendulum_sim"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# X0 - initial pendulum parameters
# 0: theta (rad)
# 1: angular velocity (rad/s)
# 2: cart position (m)
# 3: cart velocity (m/s)
X0 = [0, 0, 0, 0]


def createModel():
  model = ModelFactory.create(getModelParamsFromName('u'))
  model.enableInference({"predictedField": "u"})
  return model


def getModelParamsFromName(pendulumName):
  importName = "model_params.%s_model_params" % (
    pendulumName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % pendulumName)
  return importedModelParams


def runIoThroughNupic(model, pendulumName, plot):

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([pendulumName])
  else:
    output = nupic_output.NuPICFileOutput([pendulumName])


  # Do we need to train with data without control?
  u = 0
  t = 0
  x = X0
  counter = 0
  while True:
    counter += 1
    results = model.run({
      "theta": x[0],
      "theta_dot": x[1],
      "x": x[2],
      "x_dot": x[3],
      "u": u
    })


    if plot:
      results = shifter.shift(results) 

    prediction = results.inferences["multiStepBestPredictions"][1]
    output.write([counter], [u], [prediction])

    # retrieve next input values
    u = control(x)
    x, t = next_step(x, u, t)

  inputFile.close()
  output.close()


def runModel(pendulumName, plot=False):
  print "Creating model from %s..." % pendulumName
  model = createModel()
  runIoThroughNupic(model, pendulumName, plot)


if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(PENDULUM_NAME, plot=plot)
