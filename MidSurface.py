# EasyShells Module - API for easier Shell Model Construction in Salome
# MidSurface.py: Mid surface extraction for EasyShells module
#
# Copyright (C) 2013  Stefan Reiterer - stefan.reiterer@magnasteyr.com or maldun.finsterschreck@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from __future__ import print_function

import salome
import geompy
from numpy import array, arange 

from MyGeom.Types import *

def create_parallel_midpoints(points_lower, points_upper):
    """
    Help function to create the midpoints of two given parallel surfaces
    """
    length_u = len(points_lower[0])
    length_v = len(points_lower)

    return [[(points_lower[i][j] + points_upper[i][j])*0.5 \
              for j in range(length_u)] \
                for i in range(length_v)]

def parallel_midsurface(lower_face, upper_face, lower_deg = 2, upper_deg = 5):
    """
    Determines the midsurface of 2 parallel
    surfaces. Hereby parallel means that they
    share the same normal direction. It is assumed
    that both normals point outwards.
    """

    points_u = arange(0,1+1./upper_deg,1./upper_deg)
    points_v = points_u

    lower_points = create_local_coordinates(lower_face,points_u,points_v)  
    lower_points = create_local_coordinates(upper_face,points_u,points_v)

    midpoints = create_parallel_midpoints
