import numpy as np
import polygons_visualiser as pv
import polygons_generator as pg


def main():
    factor = 1
    num_seeds = 10

    x_min = y_min = z_min = 0
    x_max = y_max = z_max = factor
    x_lim = [x_min, x_max]
    y_lim = [y_min, y_max]
    z_lim = [z_min, z_max]

    seeds = np.random.rand(num_seeds, 3) * factor

    polygons = pg.PolyGenerator(seeds=seeds,
                                x_lim=x_lim,
                                y_lim=y_lim,
                                z_lim=z_lim
                                )

    xxx = polygons.get_polygons()

    visual = pv.PolyVisualiser(array_polygons=xxx,
                               x_lim=x_lim,
                               y_lim=y_lim,
                               z_lim=z_lim
                               )

    # visual.add_cell(vertex=True, faces=True)
    visual.animate()

    visual.show()


if __name__ == '__main__':
    main()
