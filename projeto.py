import numpy as np
import polygons_visualiser as pv
import polygons_generator as pg
from copy import copy
import polygon as p
import pickle


def get_max_x(p):
    return max(p.vertex[0])


def get_max_y(p):
    return max(p.vertex[1])


def get_max_z(p):
    return max(p.vertex[2])


def main():
    scale = 1

    x_min = y_min = z_min = 0
    x_max = y_max = z_max = scale
    x_lim = [x_min, x_max]
    y_lim = [y_min, y_max]
    z_lim = [z_min, z_max]

    filename = 'listpoly.txt'

    file_open_list = open(filename, 'rb')

    num_seeds = 40
    # seeds = np.random.rand(num_seeds, 3) * scale
    # # seeds = np.array([[1.89493127, 4.09108527, 1.83570894],
    # #                   [1.79324889, 2.50682833, 1.13780362],
    # #                   [0.86793346, 2.4029516, 3.32404097],
    # #                   [2.52394838, 0.09214482, 2.31716686],
    # #                   [2.50569309, 2.40987402, 0.5311482],
    # #                   [4.06162573, 0.45714762, 4.02152286],
    # #                   [3.23915025, 2.48641076, 4.70422564],
    # #                   [0.33169791, 3.44018418, 3.14690308],
    # #                   [0.51009783, 4.06909904, 2.9275356],
    # #                   [3.6412665, 2.17519192, 1.89861835]])
    # #
    # polygons = pg.PolyGenerator(seeds=seeds,
    #                             x_lim=x_lim,
    #                             y_lim=y_lim,
    #                             z_lim=z_lim,
    #                             scale=scale
    #                             )
    #
    # xxx = polygons.get_polygons()
    # xxx.sort(key=get_max_z)
    #
    # for i in xxx:
    #     i.rotate(np.pi / 4, np.pi / 4)
    #     i.move_to_origin()
    #
    # file_write_list = open(filename, 'wb')
    # pickle.dump(xxx, file_write_list)

    # xxx2 = pickle.load(file_open_list)

    container = [2, 2, 1]

    # paralel = np.random.rand(num_seeds, 3) * scale
    paralel = np.array([[0.28235334, 0.32376754, 0.84092732],
                        [0.61366548, 0.09302544, 0.99052983],
                        [0.1762999, 0.42781845, 0.79023381],
                        [0.94890284, 0.67306063, 0.86359112],
                        [0.93487385, 0.28900274, 0.0619199],
                        [0.07761809, 0.85646809, 0.4501854],
                        [0.05141494, 0.76069553, 0.13433091],
                        [0.97648677, 0.62783275, 0.46125964],
                        [0.02908643, 0.13860335, 0.1259358],
                        [0.27361889, 0.10862334, 0.79929282],
                        [0.70204066, 0.20059393, 0.56706984],
                        [0.98979204, 0.38391592, 0.71711026],
                        [0.01601519, 0.18133876, 0.43767359],
                        [0.84600214, 0.9338675, 0.01602098],
                        [0.17007352, 0.79854181, 0.63995873],
                        [0.91252859, 0.08059825, 0.8452045],
                        [0.37110906, 0.21449898, 0.44839036],
                        [0.36749539, 0.54441417, 0.06187667],
                        [0.25187074, 0.63458663, 0.59747453],
                        [0.49516444, 0.25685515, 0.68482676],
                        [0.04042828, 0.41315624, 0.65489867],
                        [0.94563752, 0.11412746, 0.51114823],
                        [0.02656769, 0.4796146, 0.46603509],
                        [0.65972721, 0.2533922, 0.24652541],
                        [0.73922107, 0.14490812, 0.66658445],
                        [0.46366601, 0.78402861, 0.74808383],
                        [0.21580729, 0.77518126, 0.40853229],
                        [0.02827083, 0.95874522, 0.180826],
                        [0.78392825, 0.36340276, 0.17284183],
                        [0.25689582, 0.30959101, 0.27278357],
                        [0.95379358, 0.96316886, 0.65542954],
                        [0.43344549, 0.94007984, 0.34916283],
                        [0.83858148, 0.22524851, 0.02661374],
                        [0.49072295, 0.09567852, 0.02139312],
                        [0.86086877, 0.72012403, 0.16475415],
                        [0.49353508, 0.89626124, 0.86595725],
                        [0.10540219, 0.37546821, 0.3462632],
                        [0.06090368, 0.1150828, 0.19131847],
                        [0.6190982, 0.06363157, 0.17671633],
                        [0.2134693, 0.94800653, 0.10146217]])
    xxx2 = [Retangulo(i) for i in paralel]

    ret = optimize(xxx2, container)

    obj = get_obj(ret)
    print(obj)

    showcontainer = pv.PolyVisualiser(array_polygons=ret,
                                      x_lim=container[0],
                                      y_lim=container[1],
                                      z_lim=container[2],
                                      obj=obj
                                      )
    # showcontainer.add_cell()
    showcontainer.animate()
    showcontainer.scrol()
    showcontainer.show()

    # visual = pv.PolyVisualiser(array_polygons=ret,
    #                            x_lim=x_lim,
    #                            y_lim=y_lim,
    #                            z_lim=z_lim
    #                            )
    #
    # visual.animate()
    # # visual.scrol()
    # # visual.add_cell(vertex=False, faces=True, seeds=False)
    # visual.show()


def optimize(polygons, container):
    # polygons.sort(key=get_max_y, reverse=True)
    polygons.sort(key=lambda p: p.volume, reverse=True)

    larg, comp = container[0], container[1]

    xmax, ymax, zmax = 0, 0, 0
    ylist, zlist = [], []

    for i in range(1, len(polygons)):
        atual, anterior = polygons[i], polygons[i - 1]
        xmax = get_max_x(anterior)
        ylist.append(get_max_y(anterior))
        zlist.append(get_max_z(anterior))

        if get_max_x(atual) + xmax > larg:
            xmax = 0
            ymax = max(ylist)
            ylist = []
        if get_max_y(atual) + ymax > comp:
            xmax = 0
            ymax = 0
            zmax = max(zlist)
            zlist = []

        atual.change_vertex([xmax, ymax, zmax])

    return polygons


def get_obj(pols):
    a = []
    for pol in pols:
        a.append(get_max_z(pol))

    obj = max(a)
    return obj


def Retangulo(item):
    max_x = item[0]
    max_y = item[1]
    max_z = item[2]

    vertices = [[0.0, 0.0, 0.0],
                [max_x, 0.0, 0.0],
                [0.0, max_y, 0.0],
                [max_x, max_y, 0.0],
                [0.0, 0.0, max_z],
                [max_x, 0.0, max_z],
                [0.0, max_y, max_z],
                [max_x, max_y, max_z]]

    vertices = [*zip(*vertices)]

    faces = [[1, 3, 2, 0],
             [1, 5, 7, 3],
             [1, 0, 4, 5],
             [2, 6, 4, 0],
             [2, 3, 7, 6],
             [4, 6, 7, 5]]
    volume = max_x * max_y * max_z
    ret = p.Polygon(0, vertex=vertices, faces=faces, color=item, volume=volume)
    return ret


if __name__ == '__main__':
    main()
