instance_generator
===

## Requirements

* [Pyvoro](https://github.com/wackywendell/pyvoro/) (forked by [wackywendell](wackywendell))
* [Matplotlib](https://matplotlib.org/)


## Usage Example:
### PolyGenerator:

This class generate the polygons (polyhedra) from a Voronoi's cube.

#### Importing classes:
```python
from retangulo import *
from polygon import *
from polygons_visualiser import *
```

#### Requisites:

```python
scale = 1 # factor of the cube size

# Cube size
x_min = y_min = z_min = 0
x_max = y_max = z_max = scale
x_lim = [x_min, x_max]
y_lim = [y_min, y_max]
z_lim = [z_min, z_max]

# Number of polygons
num_seeds = 60
seeds = np.random.rand(num_seeds, 3) * scale

```

#### Generating and getting the polygons

```python
# Passing arguments to constructor
# Every argument is an integer/list of integers
polygons = PolyGenerator(seeds=seeds,
			x_lim=x_lim,
			y_lim=y_lim,
			z_lim=z_lim,
			scale=scale
			)

# This will return a list of objects of type Polygon
ret = polygons.get_polygons()

```


### PolyVisualiser:

This class can show and manage an 
interactive window for data visualisation, in this case, Polygnos.

#### Importing classes:
(same as above)

#### Requisites:

```python
ret = [] # A list of Polygons
container = [4,4,4] # A list of 3 positive representing the dimensions of the visualization area
alpha=.8 # The transparency of the polygons
```

#### Generating and getting the polygons

```python
# Passing arguments to constructor
visualiser = PolyVisualiser(array_polygons=ret,
                                   x_lim=container[0],
                                   y_lim=container[1],
                                   z_lim=container[2],
                                   alpha=.8
                                   )

# This method adds the polygons to the scene
# There is an option to animate the polygons addition
visualiser.animate(no_animation=True)

# This method exibits the window plot. Nothing happens until this point
visualiser.show()

```


