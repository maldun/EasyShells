# EasyShells Module - API for easier Shell Model Construction in Salome
# MidSurface.py: Mid surface extraction for EasyShells module
#
# Copyright (C) 2013  Stefan Reiterer - stefan.reiterer@magnasteyr.com
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

def parallelMidsurface(lower_face, upper_face,lower_deg = 2 upper_deg = 5):
    """
    Determines the midsurface of 2 parallel
    surfaces. Hereby parallel means that they
    share the same normal direction. It is assumed
    that both normals point outwards.
    """

    
    #inverse = geompy.ChangeOrientation(lower_face)
    #normal = geompy.GetNormal(inverse)
    parameter_space = arange(0,1,1.0/upper_deg)
    point_creation = geompy.MakeVertexOnSurface # (arc_face, 0.5, 0.5)
    # create local coordinate systems
    points_lower = [point_creation(lower_face,u,v) \
                        for u in parameter_space for v in parameter_space]
    points_lower = [MyVertex(p) for p in points_lower] # Transform to MyGeom
    points_upper = [point_creation(upper_face,u,v) \
                        for u in parameter_space for v in parameter_space]
    points_lower = [MyVertex(p) for p in points_upper] # Transform to MyGeom
    
    # create midpoints
    [MyVertex((points_lower[i].getCoord() + points_upper[i].getCoord())/2.) for i in range(len(points_lower))]
