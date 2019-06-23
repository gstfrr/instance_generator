# -*- coding: utf-8 -*-
import pickle
import platform
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


def main(instance):
    print("Server: " + str(platform.node()) + "\n")

    # Obtem os valores do arquivo e cria os retângulos
    filename = instance
    boxes, Lu, Wu, Hu = get_data(filename)
    filename = filename.replace('.data', '', 1)
    filename = filename.replace('instances/', '', 1)
    print(filename)

    # Cria os conjuntos X,Y,Z
    BigX, BigY, BigZ = [], [], []
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

        BigX.append(p)
        BigY.append(q)
        BigZ.append(r)

    BigX = [i for i in range(sum(BigX))]
    BigY = [i for i in range(sum(BigY))]
    BigZ = [i for i in range(sum(BigZ))]

    m = Model("3D-ODRPP")

    L = m.addVar(vtype=GRB.CONTINUOUS, name="L", lb=0, ub=GRB.INFINITY)
    W = m.addVar(vtype=GRB.CONTINUOUS, name="W", lb=0, ub=GRB.INFINITY)
    H = m.addVar(vtype=GRB.CONTINUOUS, name="H", lb=0, ub=GRB.INFINITY)

    z_obj = m.addVar(vtype=GRB.CONTINUOUS, name="Z", lb=0, ub=GRB.INFINITY)

    m.addConstr(z_obj == L + W + H, "z_objective")

    m.setObjective(z_obj, GRB.MINIMIZE)

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

    # print(X, Y, Z, sep='\n')

    # Criação das variáveis binárias
    x_bin = []
    for i, box in enumerate(boxes):
        rotations = list(permutations(box.get('dim')))
        # print(box.get('dim'), rotations, sep='\t')
        k_list = []
        for k, b in enumerate(rotations):
            p_list = []
            for p in X[i]:
                q_list = []
                for q in Y[i]:
                    r_list = []
                    for r in Z[i]:
                        index = '[' + str(i) + '][' + str(k) + '][' + str(p) + '][' + str(q) + '][' + str(r) + ']'
                        x = m.addVar(vtype=GRB.BINARY, name='X_' + index)
                        r_list.append(x)
                    q_list.append(r_list)
                p_list.append(q_list)
            k_list.append(p_list)
        x_bin.append(k_list)

    print(' = Variables Added')

    # Constraint 2
    for s in BigX:
        for t in BigY:
            for u in BigZ:

                soma_r2 = LinExpr()
                for i, box in enumerate(boxes, start=0):
                    rotations = list(permutations(box.get('dim')))
                    for k, b in enumerate(rotations):
                        li, wi, hi = b[0], b[1], b[2]
                        for p in X[i]:
                            for q in Y[i]:
                                for r in Z[i]:

                                    if s - li + 1 <= p <= s:
                                        if t - wi + 1 <= q <= t:
                                            if u - hi + 1 <= r <= u:
                                                soma_r2 += x_bin[i][k][p][q][r]

                    # index = str(i)
                index = '[' + str(s) + '][' + str(t) + '][' + str(u) + ']'
                m.addConstr(soma_r2 <= 1, name='Restricao2_' + index)

    print(' = Constraint 2 adicionada')

    # Constraint 3
    for j, box in enumerate(boxes, start=0):
        bj = box.get('qtd')
        soma_r3 = LinExpr()
        rotations = list(permutations(box.get('dim')))
        for k, b in enumerate(rotations):
            for p in X[j]:
                for q in Y[j]:
                    for r in Z[j]:
                        soma_r3 += x_bin[j][k][p][q][r]
        m.addConstr(soma_r3 == bj, name='Restricao3_' + str(j))

    print(' = Constraint 3 adicionada')

    # Restrições 4, 5 e 6
    for i, box in enumerate(boxes, start=0):
        rotations = list(permutations(box.get('dim')))
        for k, b in enumerate(rotations):
            for p in X[i]:
                for q in Y[i]:
                    for r in Z[i]:
                        index = '[' + str(i) + '][' + str(k) + '][' + str(p) + '][' + str(q) + '][' + str(r) + ']'
                        li, wi, hi = b[0], b[1], b[2]
                        algo_p = (p + li) * x_bin[i][k][p][q][r]
                        algo_q = (q + wi) * x_bin[i][k][p][q][r]
                        algo_r = (r + hi) * x_bin[i][k][p][q][r]
                        m.addConstr(algo_p <= L, name='Restricao4_' + index)
                        m.addConstr(algo_q <= W, name='Restricao5_' + index)
                        m.addConstr(algo_r <= H, name='Restricao6_' + index)

    print(' = Restrições 4,5,6 adicionadas')

    m.write('models/modelo_' + filename + '.lp')
    print(' = Model written!')


if __name__ == "__main__":
    # instancia = sys.argv[1]
    instancia = 'instances/problema0.data'
    main(instancia)
