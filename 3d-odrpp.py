from bottom__front_left import *
from polygons_visualiser import PolyVisualiser
from retangulo import Retangulo
from time import time
import sys


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


def main(instancia):
    Lu, Wu, Hu = 10, 10, 10
    container = [Lu, Wu, Hu]
    boxes = get_data(instancia)
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
