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
from math import pi

SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "theta",
      "fieldType": "float",
      "maxValue": pi,
      "minValue": -pi
    },
    {
      "fieldName": "theta_dot",
      "fieldType": "float",
      "maxValue": 20,
      "minValue": -20
    },
    {
      "fieldName": "x",
      "fieldType": "float",
      "maxValue": 10,
      "minValue": -10
    },
    {
      "fieldName": "x_dot",
      "fieldType": "float",
      "maxValue": 20,
      "minValue": -20
    },
    {
      "fieldName": "u",
      "fieldType": "float",
      "maxValue": 50,
      "minValue": -50
    }
  ],
  "streamDef": {
    "info": "pendulum",
    "version": 1,
    "streams": [
      {
        "info": "ctrl_sim",
        "source": "file://ctrl_sim.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "u"
  },
  "iterationCount": -1,
  "swarmSize": "medium"
}
