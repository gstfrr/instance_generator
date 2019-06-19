import numpy as np
import polygons_visualiser as pv
from copy import copy
import polygon as p
import retangulo as r
from bottom__front_left import *
import pickle


def main():
    container = [2.5, 2, 3]

    filename = 'listpoly.txt'
    file_open_list = open(filename, 'rb')

    ret = pickle.load(file_open_list)

    # criar retângulos a partir dos poliedros de voronoi
    # paralel = []
    # for i in ret:
    #     i.move_to_origin()
    #     paralel.append([[get_max_x(i), get_max_y(i), get_max_z(i)], i.color])
    #
    # ret = [r.Retangulo(i[0], color=i[1]) for i in paralel]

    ret, obj = optimize(ret, container)
    print(obj)

    visualiser = pv.PolyVisualiser(array_polygons=ret,
                                   x_lim=container[0],
                                   y_lim=container[1],
                                   z_lim=container[2],
                                   obj=obj
                                   )

    visualiser.animate(no_animation=False)
    visualiser.scrol()
    visualiser.show()


if __name__ == '__main__':
    main()
