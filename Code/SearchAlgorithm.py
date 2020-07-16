# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1496622'
__group__ = 'DL.15'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy
import collections

def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    fi = path.last

    if(len(path.route)==1):
        fi=path.head

    for x in map.connections[fi]:
        copia = copy.deepcopy(path)
        copia.add_route(x)
        path_list.append(copia)

    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    validar=False
    ObjetoABorrar=None


    i = 0
    for x in reversed(path_list):

        for y in x.route:

            if x.route.count(y)>1:
                ObjetoABorrar=x
                validar=True

        if validar:

            path_list.remove(ObjetoABorrar)
        validar=False
        i = i + 1

    return path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
     """

    list=expand_paths+list_of_path
    return list






def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """

    Llista = [Path(origin_id)]
    C = Path(origin_id)

    while C.route[-1] != destination_id and Llista != None:
        C = Llista.pop(0)
        expand_list = expand(C, map)
        expand_list = remove_cycles(expand_list)

        Llista = insert_depth_first_search(expand_list, Llista)

    if (C.route[-1] == destination_id):
        return C
    else:
        return "NO existeix un cami per arribar-hi"







def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    list = list_of_path+expand_paths
    return list


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    Llista = [Path(origin_id)]
    C = Path(origin_id)

    while C.route[-1] != destination_id and Llista != None:
        C = Llista.pop(0)
        expand_list = expand(C, map)
        expand_list = remove_cycles(expand_list)

        Llista = insert_breadth_first_search(expand_list, Llista)

    if (C.route[-1] == destination_id):
        return C
    else:
        return "NO existeix un cami per arribar-hi"


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    if type_preference== 0:
        for x in expand_paths:

            x.update_g(1)
    elif type_preference == 1:
        for x in expand_paths:
            Dicc = map.connections[x.penultimate]
            x.update_g(Dicc[x.last])
    elif type_preference == 2:
         for x in expand_paths:
             if map.stations[x.penultimate]['name'] != map.stations[x.last]['name'] :
                res=map.connections[x.penultimate][x.last]* map.stations[x.last]['velocity']
                x.update_g(res)
    elif type_preference == 3:
        for x in expand_paths:
            if map.stations[x.last]['line'] != map.stations[x.penultimate]['line']:
                x.update_g(1)
    return expand_paths
    pass


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """

    for x in expand_paths:
        trobat = False
        i = 0
        if len(list_of_path) !=0:
         while i < len(list_of_path) and trobat != True :
            val=list_of_path[i]
            if x.g < val.g:
                list_of_path.insert(i,x)
                trobat=True
            else:
                i=i+1
        if trobat==False:
            list_of_path.append(x)



    return list_of_path
    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    Llista = [Path(origin_id)]
    C = Path(origin_id)
    i=0

    while C.route[-1] != destination_id and Llista != None:

        C = Llista.pop(0)
        expand_list = expand(C, map)
        expand_list = remove_cycles(expand_list)
        expand_list = calculate_cost(expand_list, map, type_preference)

        Llista = insert_cost(expand_list, Llista)


    if C.route[-1] == destination_id:
        return C
    else:
        return "NO existeix un cami per arribar-hi"


    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """

    if type_preference == 0:
        for x in expand_paths:
            if destination_id in x.route:
              x.update_h(0)
            else:

                x.update_h(1)
    elif type_preference == 1:

        for x in expand_paths:
          if destination_id in x.route:
              x.update_h(0)
          else:
            max = map.stations[1]['velocity']

            for y in range(1, len(map.stations)):
                val = map.stations[y]['velocity']
                if val > max:
                    max = val
            res = euclidean_dist([map.stations[x.last]['x'], map.stations[x.last]['y']], [map.stations[destination_id]['x'], map.stations[destination_id]['y']]) / max

            x.update_h(res)
    elif type_preference == 2:
         for x in expand_paths:
            if destination_id in x.route:
                x.update_h(0)

            else:
                res = euclidean_dist([map.stations[x.last]['x'], map.stations[x.last]['y']], [map.stations[destination_id]['x'], map.stations[destination_id]['y']])
                x.update_h(res)
    elif type_preference == 3:
        for x in expand_paths:
          if destination_id in x.route:
              x.update_h(0)
          else:
            if map.stations[x.last]['line'] != map.stations[x.penultimate]['line']:
                x.update_h(1)
    return expand_paths


    pass



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for x in expand_paths:
        x.f=x.g+x.h
    return expand_paths

    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths

        Codi no optim pero funcional



                DiccNegre = {'ListOfPath': [], 'Expanded_List': []}
                    val=0
    val2=0
                DiccNegre['Expanded_List'].append(val)
                val = +1
                DiccNegre['ListOfPath'].append(val2)
                val2=+1


                    i = 0
    lens =  + len(DiccNegre['ListOfPath'])
    print(len(DiccNegre['Expanded_List']))
    while i < lens-1:

        if i < len(DiccNegre['Expanded_List']):

            del expand_paths[DiccNegre['Expanded_List'][i]-1]
        else:
            print(DiccNegre['ListOfPath'][i])
            del list_of_path[DiccNegre['ListOfPath'][i]]
        i+=1


    """


    for path_expanded in reversed(expand_paths):
        if path_expanded.last in visited_stations_cost:
            if visited_stations_cost[path_expanded.last] <= path_expanded.g :
                   # expand_paths.remove(path_expanded) # NO ESTA CORRECTE AL 100% pero es lo mes optim que he trobat
                   expand_paths.remove(path_expanded)
            else:
                visited_stations_cost[path_expanded.last] = path_expanded.g # NO ESTA CORRECTE AL 100% Pero es lo mes optim que he tobat
                for x in reversed(list_of_path):

                    if path_expanded.last in x.route:
                         # NO ESTA CORRECTE AL 100% Pero es lo mes optim que he tobat
                         list_of_path.remove(x)
        else:
            visited_stations_cost[path_expanded.last] = path_expanded.g

    return expand_paths,list_of_path,visited_stations_cost

    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    for x in expand_paths:
        trobat = False
        i = 0
        if len(list_of_path) !=0:
         while i < len(list_of_path) and trobat != True :
            val=list_of_path[i]
            if x.f < val.f:
                list_of_path.insert(i,x)
                trobat=True
            else:
                i=i+1
        if trobat==False:
            list_of_path.append(x)
    return list_of_path
    pass


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    ""

    ans = map.stations[1]
    resultat_x=abs(ans['x']-coord[0])
    resultat_y=abs(ans['y']-coord[1])
    i = 2
    while i<14:

        ans=map.stations[i]
        ans_x=abs(ans['x']-coord[0])
        ans_y=abs(ans['y']-coord[1])

        if ans_x<resultat_x:
            resultat_x=ans_x
            resultat_y=ans_y
        i=i+1

    i=1
    ans = map.stations[i]
    lista=[]
    while i<14:
        i = i + 1
        ans = map.stations[i]
        ans_x = abs(ans['x']-coord[0])
        ans_y = abs(ans['y']-coord[1])
        if ans_x == resultat_x and ans_y == resultat_y:
            lista.append(i)
    if lista:
        x=0
    else:
        lista.append(1)

    return lista
        """""

    resultat_x = euclidean_dist([map.stations[1]['x'], map.stations[1]['y']], coord)
    Lista=[1]
    i = 2
    while i < len(map.stations)+1:
        ans = euclidean_dist([map.stations[i]['x'], map.stations[i]['y']], coord)

        if ans < resultat_x:
            Lista = []
            Lista.append(i)
            resultat_x = ans
        elif ans == resultat_x:
            Lista.append(i)
        i = i+1

    return Lista

def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    origin_id=coord2station(origin_coor,map)[0]
    destination_id=coord2station(dest_coor,map)[0]

    Llista = [Path(origin_id)]
    C = Path(origin_id)
    visited_stations_cost={origin_id : 0}
    while C.route[-1] != destination_id and Llista != None:

        C = Llista.pop(0)
        expand_list = expand(C, map)
        expand_list = remove_cycles(expand_list)
        expand_list = calculate_cost(expand_list, map, type_preference)
        expand_list, Llista, visited_stations_cost = remove_redundant_paths(expand_list, Llista, visited_stations_cost)
        expand_list=calculate_heuristics(expand_list,map,destination_id,type_preference)
        expand_list=update_f(expand_list)
        Llista = insert_cost_f(expand_list, Llista)

    if C.route[-1] == destination_id:
        print(C)
        return C
    else:
        return "NO existeix un cami per arribar-hi"





    pass