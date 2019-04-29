from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors, animation
import pyvoro

# scale of cube
factor = 1

dots_num = 10


def get_polygons():
    # Generate Voronoi cells
    cells = pyvoro.compute_voronoi(
        points=dots,
        limits=[[x_min, x_max], [y_min, y_max], [z_min, z_max]],
        dispersion=1
    )

    polygon_list = []
    for key, cell in enumerate(cells):
        ve = get_vertices(cell)
        fa = get_faces(cell['faces'])
        co = np.random.rand(dots_num, 3)
        polygon_list.append([ve, fa, co])

    return polygon_list


def add_seeds(points):
    ax.scatter(
        points[0], points[1], points[2],
        c='b',
        marker='o'
    )
    return None


def add_cell(cell):
    vertices, faces, color = cell[0], cell[1], cell[2]
    add_vertex(vertices, color)
    add_faces(faces, vertices, color)
    return None


def add_vertex(vertices, color):
    # print(vertices)
    ax.scatter(
        vertices[0], vertices[1], vertices[2],
        c='w',
        marker='.',
        alpha=0
    )
    return None


def new_face(augusto, color):
    augusto = [*zip(*augusto)]
    x = augusto[0]
    y = augusto[1]
    z = augusto[2]
    verts2 = [list(zip(x, y, z))]
    collection = Poly3DCollection(verts2, alpha=0.33)
    collection.set_facecolor(color)
    collection.set_edgecolor(color)
    ax.add_collection3d(collection, zs='z')
    return None


def add_faces(faces, vertices, color):
    vertices = [*zip(*vertices)]
    for f in faces:
        augusto = []
        for i in f:
            augusto.append(vertices[i])
        new_face(augusto, color)

    return None


def get_vertices(vertex_dict):
    v = []
    for i in vertex_dict['vertices']:
        v.append(tuple(i))

    return [*zip(*v)]


def get_faces(l):
    f = []
    for i in l:
        f.append(i['vertices'])
    return f


# Limits
x_min = y_min = z_min = 0
x_max = y_max = z_max = factor

x_lim = [x_min, x_max]
y_lim = [y_min, y_max]
z_lim = [z_min, z_max]

# Seeds
dots = np.random.rand(dots_num, 3) * factor
dots_t = [*zip(*dots)]

# make color map (unnecessary for just random colorization)

fig = plt.figure(figsize=(10, 6.5))
ax = fig.add_subplot(111, projection='3d', aspect='equal')
ax.set_xlim3d(x_lim)
ax.set_ylim3d(y_lim)
ax.set_zlim3d(z_lim)

# add_seeds(dots_t)

poly = get_polygons()


def update_lines(num):
    add_cell(poly[num])


line_ani = animation.FuncAnimation(fig, update_lines, frames=dots_num, interval=500, repeat=False)

plt.show()
