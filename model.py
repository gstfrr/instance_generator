# -*- coding: utf-8 -*-

import platform
from polygons_visualiser import PolyVisualiser
from retangulo import Retangulo
from itertools import permutations
import numpy as np

from gurobipy import *


def main():
    print("Server: " + str(platform.node()) + "\n")

    Lu, Wu, Hu = 28, 26, 6
    container = [Lu, Hu, Hu]

    m = Model("3D-ODRPP")
    m.setParam('TimeLimit', 60.0)

    L = m.addVar(vtype=GRB.CONTINUOUS, name="L", lb=0, ub=GRB.INFINITY)
    W = m.addVar(vtype=GRB.CONTINUOUS, name="W", lb=0, ub=GRB.INFINITY)
    H = m.addVar(vtype=GRB.CONTINUOUS, name="H", lb=0, ub=GRB.INFINITY)
    z_obj = m.addVar(vtype=GRB.CONTINUOUS, name="Z", lb=0, ub=GRB.INFINITY)
    m.addConstr(z_obj, GRB.EQUAL, L + W + H, "z_objective")
    m.setObjective(z_obj, GRB.MINIMIZE)

    boxes = get_data('problema1.data')

    X, Y, Z = [], [], []
    for i in boxes:  # Percorrer cada tipo de caixa
        p, q, r = 0, 0, 0
        for e in range(1, i.get('qtd') + 1):
            l = i.get('dim')[0]
            p += e * l
        for e in range(1, i.get('qtd') + 1):
            l = i.get('dim')[1]
            q += e * l
        for e in range(1, i.get('qtd') + 1):
            l = i.get('dim')[2]
            r += e * l

        X.append(p)
        Y.append(q)
        Z.append(r)

    x_bin = []
    for i, box in enumerate(boxes, start=0):
        p_list = []
        for p in range(X[i]):
            q_list = []
            for q in range(Y[i]):
                r_list = []
                for r in range(Z[i]):
                    index = '['+str(i) + '][' + str(p) + '][' + str(q) + '][' + str(r)+']'
                    x = m.addVar(vtype=GRB.BINARY, name='X_' + index)
                    r_list.append(x)
                q_list.append(r_list)
            p_list.append(q_list)
        x_bin.append(p_list)

    for j, box in enumerate(boxes, start=0):
        bj = box.get('qtd')
        soma = LinExpr()
        for p in range(X[j]):
            for q in range(Y[j]):
                for r in range(Z[j]):
                    soma += x_bin[j][p][q][r]
        m.addConstr(soma, GRB.EQUAL, bj, name='Restricao3_' + str(j))

    for i, box in enumerate(boxes, start=0):
        for p in range(X[i]):
            for q in range(Y[i]):
                for r in range(Z[i]):
                    index = '['+str(i) + '][' + str(p) + '][' + str(q) + '][' + str(r)+']'
                    algo_p = (p + box.get('dim')[0]) * x_bin[i][p][q][r]
                    algo_q = (q + box.get('dim')[1]) * x_bin[i][p][q][r]
                    algo_r = (r + box.get('dim')[2]) * x_bin[i][p][q][r]
                    m.addConstr(algo_p, GRB.LESS_EQUAL, L, name='Restricao4_' + index)
                    m.addConstr(algo_q, GRB.LESS_EQUAL, W, name='Restricao5_' + index)
                    m.addConstr(algo_r, GRB.LESS_EQUAL, H, name='Restricao6_' + index)

    # for i, box in enumerate(boxes, start=0):
    #     for p in range(X[i]):
    #         for q in range(Y[i]):
    #             for r in range(Z[i]):
    #                 index = '['+str(i) + '][' + str(p) + '][' + str(q) + '][' + str(r)+']'
    #                 m.addConstr(x_bin[i][p][q][r], GRB.LESS_EQUAL, 1, name='Restricao2_' + index)

    m.write('modelo' + '.lp')
    m.optimize()
    print('\nFunção objetivo: ', str(round(L.X)), str(round(W.X)), str(round(W.X)), sep='\t')

    solutions = []
    for i, box in enumerate(boxes, start=0):
        for p in range(X[i]):
            for q in range(Y[i]):
                for r in range(Z[i]):
                    if x_bin[i][p][q][r].X == 1:
                        solutions.append([p, q, r])

    for i in solutions:
        print(i)

    # visualiser = PolyVisualiser(array_polygons=ret,
    #                             x_lim=container[0],
    #                             y_lim=container[1],
    #                             z_lim=container[2],
    #                             # obj=obj
    #                             )
    #
    # visualiser.animate(no_animation=False)
    # visualiser.scrol()
    # visualiser.show()


def get_data(datafile: str) -> list:
    filename = datafile
    file_open_list = open(filename, 'r')

    boxes = []
    for line in file_open_list:
        b = [int(i) for i in line.split(sep='\t')]
        # dim = list(permutations(b[1:4]))
        dim = b[1:4]
        b = {'type': b[0],
             'dim': dim,
             'qtd': b[4]}
        # for i in range(num):
        boxes.append(b)

    return boxes


if __name__ == "__main__":
    main()
