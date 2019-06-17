import polygons_generator as pg
from bottom__front_left import *
import pickle


def main():
    scale = 1

    x_min = y_min = z_min = 0
    x_max = y_max = z_max = scale
    x_lim = [x_min, x_max]
    y_lim = [y_min, y_max]
    z_lim = [z_min, z_max]

    filename = 'listpoly.txt'

    num_seeds = 40
    seeds = np.random.rand(num_seeds, 3) * scale
    # seeds = np.array([[1.89493127, 4.09108527, 1.83570894],
    #                   [1.79324889, 2.50682833, 1.13780362],
    #                   [0.86793346, 2.4029516, 3.32404097],
    #                   [2.52394838, 0.09214482, 2.31716686],
    #                   [2.50569309, 2.40987402, 0.5311482],
    #                   [4.06162573, 0.45714762, 4.02152286],
    #                   [3.23915025, 2.48641076, 4.70422564],
    #                   [0.33169791, 3.44018418, 3.14690308],
    #                   [0.51009783, 4.06909904, 2.9275356],
    #                   [3.6412665, 2.17519192, 1.89861835]])

    polygons = pg.PolyGenerator(seeds=seeds,
                                x_lim=x_lim,
                                y_lim=y_lim,
                                z_lim=z_lim,
                                scale=scale
                                )

    ret = polygons.get_polygons()

    file_write_list = open(filename, 'wb')
    pickle.dump(ret, file_write_list)


if __name__ == '__main__':
    main()
