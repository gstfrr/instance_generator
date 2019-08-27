from bottom__front_left import *
from polygons_visualiser import PolyVisualiser
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

    now = time()
    ret, obj = optimize(ret, container)
    obj = get_obj(ret)
    print('Time: ' + str(time() - now))

    print('Dimensoes: ', Lu, Wu, Hu)
    print('Função objetivo: ' + str(obj))

    x_lim = max(Lu, Wu, obj)
    y_lim = max(Lu, Wu, obj)
    z_lim = max(Lu, Wu, obj)

    visualiser = PolyVisualiser(array_polygons=ret,
                                x_lim=x_lim,
                                y_lim=y_lim,
                                z_lim=z_lim,
                                obj=obj,
                                alpha=1,
                                title=instancia,
                                )

    visualiser.animate(no_animation=False)
    visualiser.scrol()
    visualiser.show()


if __name__ == "__main__":
    # instancia = sys.argv[1]
    instancia = 'instances/problema0.data'
    main(instancia)
