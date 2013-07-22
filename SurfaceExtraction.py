# EasyShells Module - API for easier Shell Model Construction in Salome
# SurfaceExtraction.py : Module for extraction groups of certain faces
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

from MyGeom.Types import *
from MyGeom.Tools import inner_product, explode_sub_shape

def check_turned_away_face_from_plane(face,plane_normal,local_sys = None):
    """
    Definition: A face is called turned away from a plane
               iff <n_p,n_f(x)> > 0 for all x in
               the face, where n_p is the normal
               of the plane, and n_f(x) the normal of
               the face in a point x
    """
    if local_sys is None:
        if inner_product(face.getNormal(),plane_normal) > 0.0:
            return True
        else:
            return False
    else:
        raise NotImplementedError("Error: More Precise checks are not implemented yet!")

def get_turned_away_shell_faces_from_plane(shell,plane,to_face = False):

    if to_face: # If the faces look into the direction of the plane
        plane_normal = (plane.changeOrientation(make_copy = True)).getNormal()
    else:
        plane_normal = plane.getNormal()

    faces = explode_sub_shape(shell,"FACE",add_to_study = False)
    faces = [MyFace(face) for face in faces]
    turned_away = [face for face in faces if check_turned_away_face_from_plane(face,plane_normal)]

    return turned_away

def get_inner_side_of_shell(shell):
    """
    Takes a closed shell of faces and return the faces which lie on the
    inner side. E.g. pipes or tanks etc. 
    """

    pass
