import numpy as np

OPT_X = 1
OPT_y = 2
OPT_Z = 3
OPT_V = 4


def get_max_x(p):
    return max(p.vertex[0])


def get_max_y(p):
    return max(p.vertex[1])


def get_max_z(p):
    return max(p.vertex[2])


def get_obj(pols):
    a = []
    for pol in pols:
        a.append(get_max_z(pol))

    obj = max(a)
    return obj


def optimize(polygons, container):
    solutions = []
    for i in range(4):
        sol = optimizer(polygons, container, sort_mode=i)
        obj = get_obj(sol)
        solutions.append([sol, obj])
        print(i, obj)

    best = min(solutions, key=lambda x: x[1])
    return best


def optimizer(polygons, container, sort_mode=0):
    width, length = container[0], container[1]

    if sort_mode == 0:
        polygons.sort(key=get_max_x, reverse=False)
    elif sort_mode == 1:
        polygons.sort(key=get_max_y, reverse=False)
    elif sort_mode == 2:
        polygons.sort(key=get_max_z, reverse=False)
    elif sort_mode == 3:
        polygons.sort(key=lambda p: p.volume, reverse=False)

    for pol in polygons:
        # print(type(pol))
        x, y, z = get_max_x(pol), get_max_y(pol), get_max_z(pol)

        if z > x or z > y:
            pol.rotate(0, np.pi / 2)
        if x > y:
            pol.rotate(np.pi / 2, 0)

        pol.move_to_origin()

    xmax, ymax, zmax = 0, 0, 0
    ylist, zlist = [], []

    for i in range(1, len(polygons)):
        atual, anterior = polygons[i], polygons[i - 1]
        xmax = get_max_x(anterior)
        ylist.append(get_max_y(anterior))
        zlist.append(get_max_z(anterior))

        if get_max_x(atual) + xmax > width:
            xmax = 0
            ymax = max(ylist)
            ylist = []
        if get_max_y(atual) + ymax > length:
            xmax = 0
            ymax = 0
            zmax = max(zlist)
            zlist = []

        atual.change_vertex([xmax, ymax, zmax])
        # print(xmax, ymax, zmax, sep='\t\t')

    return polygons
