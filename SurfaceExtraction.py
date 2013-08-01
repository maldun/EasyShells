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
from MyGeom.Tools import *

def check_turned_away_face_from_plane(face,plane_normal,sign = 1.0, local_sys = None, strict = False):
    """
    Definition: A face is called turned away from a plane
               iff <n_p,n_f(x)> >= 0 for all x in
               the face, where n_p is the normal
               of the plane, and n_f(x) the normal of
               the face in a point x.
               Analogously: A face is called strictly
               turned away iff <n_p,n_f(x)> > 0 for
               all x in the face.
    """
    if local_sys is None:
        if strict:
            if sign*inner_product(face.getNormal(),plane_normal) > 0.0:
                return True
            else:
                return False
        else:
            if sign*inner_product(face.getNormal(),plane_normal) >= 0.0:
                return True
            else:
                return False
    else:
        raise NotImplementedError("Error: More Precise checks are not implemented yet!")

def get_turned_away_shell_faces_from_plane(shell,plane,to_face = False, strict = False):

    if to_face: # If the faces look into the direction of the plane
        sign = -1.0
    else:
        sign = 1.0
    
    plane_normal = plane.getNormal()

    faces = explode_sub_shape(shell,"FACE",add_to_study = False)
    faces = [MyFace(face) for face in faces]
    turned_away = [face for face in faces \
                       if check_turned_away_face_from_plane(face,plane_normal,sign = sign, strict = strict)]
    
    return turned_away

def check_neighbour(face1,face2):
    """
    checks if two faces are neighbours. If one of the two faces is none also return False
    """
    if face1 is None or face2 is None:
        return False
    
    if get_min_distance(face1,face2) == 0.0:
        if face1 != face2:
            return True

    return False

def get_inner_side_of_shell(shell, inner_face, border_faces = [], return_shell = False):
    """
    Takes a closed shell of faces and return the faces which lie on the
    inner side. E.g. pipes or tanks etc. This Version needs the faces
    which serves as border, and one face which lies on the inner

    Algorithm : We remove all borders from the faces. Then get all neighbours
                of the inner face. These are marked now and will be removed
                from the face list. The inner face will then marked as done 
                Then for each marked face get the neighbours and mark them
                and then set this face done.
                This will be until if there are no more faces to mark.
                
    """
    
    if not border_faces:
        raise NotImplementedError("Error: Automatic determination of borders is not implemented yet!")

    if isinstance(shell,list):
        face_list = list(shell) # copy shell
    else:
        shell = MyShell(shell)
        face_list = explode_sub_shape(shell,"FACE",add_to_study = False)

    # convert to MyFaces
    face_list = [MyFace(face) for face in face_list]
    # filter out faces which are not in the border list
    face_list = [face for face in face_list if not face in border_faces]

    marked = [inner_face]
    done = []
    counter = 0
    while True:
        
        marked_face = marked.pop()
        # get neigbour indices
        indices = [i for i in range(len(face_list)) \
                       if check_neighbour(marked_face,face_list[i]) is True]
        

        # filter out new_neighbours
        new_neighbours = [face_list[i] for i in indices ]
        for i in indices:
            face_list[i] = None

        face_list = [face for face in face_list if not face is None]

        marked += new_neighbours
        done += [marked_face]

        print(" Length marked: ", len(marked), " Length done: ", len(done))
        print(counter)
        counter += 1
        if marked == []:
            if return_shell:
                return MyShell(done)
            else:
                return done

def filter_list_by_radius(center_face,face_list,radius):
    inner = []
    outer = []

    for face in face_list:
        if get_min_distance(center_face,face) <= radius:
            inner += [face]
        else:
            outer += [face]

    return inner, outer

def get_inner_side_of_shell_with_radius(shell, inner_face, radius, border_faces = []):
    """
    Takes a closed shell of faces and return the faces which lie on the
    inner side. E.g. pipes or tanks etc. This Version needs the faces
    which serves as border, and one face which lies on the inner

    Algorithm : We remove all borders from the faces. Then get all neighbours
                of the inner face. These are marked now and will be removed
                from the face list. The inner face will then marked as done 
                Then for each marked face get the neighbours and mark them
                and then set this face done.
                This will be done until there are no more faces to mark.
                
    """
    
    if not border_faces:
        raise NotImplementedError("Error: Automatic determination of borders is not implemented yet!")

    shell = MyShell(shell)
    face_list = explode_sub_shape(shell,"FACE",add_to_study = False)
    face_list = [MyFace(face) for face in face_list]
    # filter out faces which are not in the border list
    face_list = [face for face in face_list if not face in border_faces]
    
    marked = [inner_face]
    done = []
    counter = 0
    while True:
        
        filtered_face_list, face_list = filter_list_by_radius(marked[-1],face_list,radius)
        done += get_inner_side_of_shell(marked[-1],filtered_face_list)

        for done_face in done:
            for face in face_list:
                if check_neighbour(done_face,face) is True:
                    marked += [face]
                    found = True
                    break
            if found:
                break
        else:
            return done
                
            
