#  -*- coding: utf-8 -*-

from __future__ import print_function

import salome
import geompy
import smesh
from numpy import array, arange, cross
from numpy.linalg import norm

from MyGeom.Types import *

# EasyShells Module - API for easier Shell Model Construction in Salome
# MidSurface.py: Mid surface extraction for EasyShells module
#
# Copyright (C) 2013  Stefan Reiterer - maldun.finsterschreck@gmail.com
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

def computeLinearNormals(face,Mesh):
    """
    Computes the normal vector of a linear face
    """

    nodes = Mesh.GetElemNodes(face)
    p0 = Mesh.GetNodeXYZ(nodes[0])
    p1 = Mesh.GetNodeXYZ(nodes[1])
    p2 = Mesh.GetNodeXYZ(nodes[-1])

    vec1 = array(p1) - numpy.array(p0)
    vec2 = array(p2) - numpy.array(p0)
    vec_normal = cross(vec1, vec2)
    return vec_normal/norm(vec_normal)


