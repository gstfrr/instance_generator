import numpy as np
import polygons_visualiser as pv
import polygons_generator as pg
import pymesh as pm
from copy import copy
import polygon as p
import retangulo as r
from bottom__front_left import *
import pickle


def main():
    container = [60, 60, 60]
    num_seeds = 5

    scale = 50

    x_min = y_min = z_min = 0
    x_max = y_max = z_max = scale
    x_lim = [x_min, x_max]
    y_lim = [y_min, y_max]
    z_lim = [z_min, z_max]

    seeds = np.random.rand(num_seeds, 3) * scale
    polygons = pg.PolyGenerator(seeds=seeds, x_lim=x_lim, y_lim=y_lim, z_lim=z_lim, scale=scale)
    ret = polygons.get_polygons()

    filename = '5piece_poly.txt'
    # file_write_list = open(filename, 'wb')
    # pickle.dump(ret, file_write_list)

    file_read_list = open(filename, 'rb')
    ret = pickle.load(file_read_list)
    ret = ret[0]
    # ret = ret[0:1]

    vertices = [*zip(*ret.vertex)]
    vertices = [list(i) for i in vertices]
    vertices = np.array(vertices)
    print('TYPE VERTICES:', type(vertices), type(vertices[0]))

    # faces=[]
    # for i in ret.faces:
    #     a = np.array(i)
    #     faces.append(a)
    #     print(a,type(a),sep='\t')
    #
    # faces = np.array(faces)
    # faces = faces.transpose()
    # # faces=[]
    # # faces = np.array(faces)
    # print('Faces:\n', faces)
    # print('TYPE FACES:   ', faces.ndim, faces.shape, type(faces), type(faces[0]))

    faces = np.array([
        [0, 3, 2, 1],  # bottom
        [4, 5, 6, 7],  # top
        [1, 2, 6, 5],  # right
        [0, 4, 7, 3],  # left
        [0, 1, 5, 4],  # front
        [7, 6, 2, 3],  # back
    ])
    print('Faces:\n', faces)
    print('TYPE FACES:   ', faces.ndim, faces.shape, type(faces), type(faces[0]))



    print('\n\n\n')
    mesh = pm.form_mesh(vertices, faces)
    # print(mesh)
    # print(mesh.vertices)
    # print(mesh.faces)

    # visualiser = pv.PolyVisualiser(array_polygons=ret,
    #                                x_lim=container[0],
    #                                y_lim=container[1],
    #                                z_lim=container[2],
    #                                obj=obj,
    #                                alpha=.8
    #                                )
    #
    # visualiser.animate(no_animation=False)
    # visualiser.scrol()
    # visualiser.show()


if __name__ == '__main__':
    main()
