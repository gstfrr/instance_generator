# -*- coding: utf-8 -*-

import platform
from polygons_visualiser import PolyVisualiser
from retangulo import Retangulo
from itertools import permutations
import numpy as np
from gurobipy import *


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


def main():
    print("Server: " + str(platform.node()) + "\n")

    # Obtem os valores do arquivo e cria os retângulos
    filename = 'problema0.data'
    boxes = get_data(filename)
    filename = filename.replace('.data', '', 1)

    ret = []
    for b in boxes:
        color_b = np.random.rand(1, 3)
        for i in range(b.get('qtd')):
            ret.append(Retangulo(b.get('dim'), color=color_b))

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

    # print(BigX, BigY, BigZ, sep='\n')

    Lu, Wu, Hu = 10, 10, 10
    container = [Lu, Wu, Hu]

    m = Model("3D-ODRPP")
    m.setParam('TimeLimit', 50 * 60.0)

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
        p_list = []
        for p in X[i]:
            q_list = []
            for q in Y[i]:
                r_list = []
                for r in Z[i]:
                    index = '[' + str(i) + '][' + str(p) + '][' + str(q) + '][' + str(r) + ']'
                    x = m.addVar(vtype=GRB.BINARY, name='X_' + index)
                    r_list.append(x)
                q_list.append(r_list)
            p_list.append(q_list)
        x_bin.append(p_list)

    print(' = Variáveis criadas')

    # Restrição 2
    for s in BigX:
        for t in BigY:
            for u in BigZ:

                soma_r2 = LinExpr()
                for i, box in enumerate(boxes, start=0):
                    li, wi, hi = box.get('dim')[0], box.get('dim')[1], box.get('dim')[2]
                    for p in X[i]:
                        for q in Y[i]:
                            for r in Z[i]:

                                if s - li + 1 <= p <= s:
                                    if t - wi + 1 <= q <= t:
                                        if u - hi + 1 <= r <= u:
                                            soma_r2 += x_bin[i][p][q][r]

                # index = str(i)
                index = '[' + str(s) + '][' + str(t) + '][' + str(u) + ']'
                m.addConstr(soma_r2 <= 1, name='Restricao2_' + index)

    print(' = Restrição 2 adicionada')

    # Restrição 3
    for j, box in enumerate(boxes, start=0):
        bj = box.get('qtd')
        soma_r3 = LinExpr()
        for p in X[j]:
            for q in Y[j]:
                for r in Z[j]:
                    soma_r3 += x_bin[j][p][q][r]
        m.addConstr(soma_r3 == bj, name='Restricao3_' + str(j))

    print(' = Restrição 3 adicionada')

    # Restrições 4, 5 e 6
    for i, box in enumerate(boxes, start=0):
        for p in X[i]:
            for q in Y[i]:
                for r in Z[i]:
                    index = '[' + str(i) + '][' + str(p) + '][' + str(q) + '][' + str(r) + ']'
                    li, wi, hi = box.get('dim')[0], box.get('dim')[1], box.get('dim')[2]
                    algo_p = (p + li) * x_bin[i][p][q][r]
                    algo_q = (q + wi) * x_bin[i][p][q][r]
                    algo_r = (r + hi) * x_bin[i][p][q][r]
                    m.addConstr(algo_p <= L, name='Restricao4_' + index)
                    m.addConstr(algo_q <= W, name='Restricao5_' + index)
                    m.addConstr(algo_r <= H, name='Restricao6_' + index)

    print(' = Restrições 4,5,6 adicionadas')

    m.write('modelo_' + filename + '.lp')
    print(' = Model written!')
    m.optimize()

    if m.status == GRB.Status.OPTIMAL:
        m.write('resultado_' + filename + '.sol')

        print('\nFunção objetivo: ', str(round(L.X)), str(round(W.X)), str(round(W.X)), sep='\t')

        # Recupera as posições das caixas
        solutions = []
        for i, box in enumerate(boxes, start=0):
            for p in X[i]:
                for q in Y[i]:
                    for r in Z[i]:
                        if x_bin[i][p][q][r].X == 1:
                            solutions.append([i, (p, q, r)])

        # Aplica a soluções aos retângulos conhecidos
        for i, r in enumerate(ret):
            print(solutions[i])
            r.change_vertex(list(solutions[i][1]))

        visualiser = PolyVisualiser(array_polygons=ret,
                                    x_lim=container[0],
                                    y_lim=container[1],
                                    z_lim=container[2],
                                    # obj=obj,
                                    alpha=.5
                                    )

        visualiser.animate(no_animation=False)
        visualiser.scrol()
        visualiser.show()


if __name__ == "__main__":
    main()
