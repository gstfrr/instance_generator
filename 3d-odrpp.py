from bottom__front_left import *
# from polygons_visualiser import PolyVisualiser
from retangulo import Retangulo
from time import time
import sys


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


def main(instancia):
    boxes, Lu, Wu, Hu = get_data(instancia)
    container = [Lu, Wu, Hu]
    ret = []
    for b in boxes:
        color_i = np.random.rand(1, 3)
        for i in range(b.get('qtd')):
            ret.append(Retangulo(b.get('dim'), color=color_i))

    ret, obj = optimize(ret, container)
    print('Função objetivo: ' + str(obj))

    # visualiser = PolyVisualiser(array_polygons=ret,
    #                             x_lim=container[0],
    #                             y_lim=container[1],
    #                             z_lim=container[2],
    #                             obj=obj,
    #                             alpha=.5
    #                             )
    #
    # visualiser.animate(no_animation=False)
    # visualiser.scrol()
    # visualiser.show()


if __name__ == "__main__":
    now = time()
    instancia = sys.argv[1]
    nome_saida = 'results/saida_BFL_' + instancia.replace('.data', '')
    nome_saida = nome_saida.replace('instances/', '')
    sys.stdout = open(nome_saida + '.txt', "w")
    main(instancia)
    print('Time: ' + str(time() - now))
