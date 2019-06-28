# -*- coding: utf-8 -*-
import pickle
import platform
from polygons_visualiser import PolyVisualiser
from retangulo import Retangulo
from itertools import permutations
import numpy as np
from gurobipy import *


def get_data(datafile):
    filename = datafile
    file_open_list = open(filename, 'r')

    boxes = []
    for line in file_open_list:
        b = [int(i) for i in line.split(sep='\t')]
        boxes.append(b)

    Lu, Wu, Hu = boxes[-1][0], boxes[-1][1], boxes[-1][2]
    boxes.pop()

    boxes2 = []
    for b in boxes:
        dim = b[1:4]
        b = {'type': b[0],
             'dim': dim,
             'qtd': b[4]}
        boxes2.append(b)

    return boxes2, Lu, Wu, Hu


def main(instance, model_file):
    print("Server: " + str(platform.node()) + "\n")

    # Obtem os valores do arquivo e cria os retângulos
    filename = instance
    boxes, Lu, Wu, Hu = get_data(filename)
    filename = filename.replace('.data', '', 1)
    filename = filename.replace('instances/', '', 1)
    print(filename)

    m = read(model_file)
    print('Problema: ' + m.getAttr('modelName'))
    m.setParam('TimeLimit', 1 * 3600.0)

    vars = m.getVars()
    z_obj, L, W, H = vars[0], vars[1], vars[2], vars[3]

    X, Y, Z = [], [], []
    for i, box in enumerate(boxes, start=0):
        li = box.get('dim')[0]
        wi = box.get('dim')[1]
        hi = box.get('dim')[2]
        X_i = [p for p in range(0, Lu - li)]
        Y_i = [p for p in range(0, Wu - wi)]
        Z_i = [p for p in range(0, Hu - hi)]
        X.append(X_i)
        Y.append(Y_i)
        Z.append(Z_i)

    m.optimize()

    # Recuperar as variáveis binárias
    x_bin = []
    for i, box in enumerate(boxes):
        rotations = list(permutations(box.get('dim')))
        k_list = []
        for k, b in enumerate(rotations):
            p_list = []
            for p in X[i]:
                q_list = []
                for q in Y[i]:
                    r_list = []
                    for r in Z[i]:
                        index = 'X_' + '{}_{}_{}_{}_{}'.format(i, k, p, q, r)
                        x = m.getVarByName(index)
                        r_list.append(x)
                    q_list.append(r_list)
                p_list.append(q_list)
            k_list.append(p_list)
        x_bin.append(k_list)

    print(' = Variables Added')

    if True:
        m.write('results/resultado_' + filename + '.sol')
        print('Container: ', Lu, Wu, Hu, sep='\t')
        container = [Lu, Wu, z_obj.X]
        print('\nFunção objetivo: ', container[0], container[1], container[2], sep='\t')

        # Recupera as posições das caixas
        solutions = []
        for i, box in enumerate(boxes, start=0):
            sol_box = []
            for k in range(6):
                for p in X[i]:
                    for q in Y[i]:
                        for r in Z[i]:
                            if x_bin[i][k][p][q][r].X == 1:
                                sol_box.append([i, (p, q, r), k])
            solutions.append(sol_box)

        ret = []
        for i, box in enumerate(boxes):
            color_b = np.random.rand(1, 3)
            rotated_box = list(permutations(box.get('dim')))
            for j in range(box.get('qtd')):
                sol = solutions[i][j]
                r = rotated_box[sol[2]]
                r = Retangulo(vertex=r, color=color_b)
                r.change_vertex(list(sol[1]))
                ret.append(r)

        ret.sort(key=lambda x: max(x.vertex[2]), reverse=True)

        file_write_list = open('results/retangulos_' + filename + '.bin', 'wb')
        pickle.dump(ret, file_write_list)

        visualiser = PolyVisualiser(array_polygons=ret,
                                    x_lim=container[0],
                                    y_lim=container[1],
                                    z_lim=container[2],
                                    obj=container[2],
                                    alpha=.8,
                                    title=filename,
                                    )

        visualiser.animate(no_animation=False)
        visualiser.scrol()
        visualiser.show()


if __name__ == "__main__":
    instancia = sys.argv[1]
    modelo = sys.argv[2]
    # instancia = 'instances/problema0.data'
    # modelo = 'models/modelo_CUT_problema0.lp'
    main(instancia, modelo)
