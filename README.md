# Faerun (Python)

Faerun (Python) is based on the [Lore.js](https://github.com/reymond-group/lore) 3D WebGL engine for interactive big data rendering and the [FUn](http://doc.gdb.tools/fun/) project. It facilitates the creation of interactive (2D and 3D) HTML plots of chemical data (or chemical spaces). Molecular structures are rendered using [SmilesDrawer](https://github.com/reymond-group/smilesDrawer).

**Associated Publication**: https://academic.oup.com/bioinformatics/article/34/8/1433/4657075

<img alt="Faerun Python" src="http://doc.gdb.tools/faerun-python/intro.png"></img>

## Installation

Faerun can be installed using pip.

```bash
pip install faerun
```

In order to use it in a script, the class `Faerun` has to be imported from the package.

```python
from faerun import Faerun
```

That’s it for the installation.

## Create a Plot Document

In order to plot, a plot document has to be created. To do so, create an instance of the class `Faerun`

```python
from faerun import Faerun

f = Faerun(title='faerun-example', clear_color='#222222', coords=False, view='free')
```

Here, we set the `title` of the plot document. This will be used as the title of the HTML document. The clear color of the canvas, which is the background color of the plot, is set to `'#222222'` (which is the hex-code for a dark gray).
The drawing of coordinate axes is disabled by setting `coords=False` and since we want to draw 3D data, the argument `view` is set to `'free'` to enable the user to pan and rotate the plot.

## Preparing Data for Plotting

The next step is to prepare the data which is to be plotted. In the tutorial, we will just generate some nice looking data using `numpy`.

```python
import numpy as np

x = np.linspace(0, 12.0, 326)
y = np.sin(np.pi * x)
z = np.cos(np.pi * x)
c = np.random.randint(0, 6, len(x))
```

This data can then be wrapped in a `dict`. In addition, `DataFrame` from the `pandas` package are also supported by faerun.
In the example, the same values are used for the colors `c` and labels `labels`.

```python
data = {'x': x, 'y': y, 'z': z, 'c': c, 'labels': c}
```

## Adding a Scatter Layer

Given the `Faerun` instance and the data, a scatter plot can be created using the method `add_scatter`.

```python
f.add_scatter('helix', data, shader='sphere', colormap='Dark2', point_scale=5.0,
              categorical=True, has_legend=True, legend_labels=[(0, 'Zero'), (1, 'One')])
```

The data is added as a scatter layer named helix. The chose shader will render the data points as
spheres (with diffuse and specular lighting) of size 5.0 with colors from the `matplotlib` colormap `'Dark2'`.
As the `c` is categorical, the parameter `categorical` is set to `True`, otherwise `matplotlib` will mess up the values.

Finally, `has_legend=True` adds the scatter layer to the legend and `legend_labels` is a `list` of `tuple`, associating values with a label.

## Saving to HTML

The faerun document can the be plotted to an HTML document with an accompanying JavaScript data file.

```python
f.plot('helix')
```

This saves the plot as `helix.html\` and \`\`helix.js`. The files can be opened locally or hosted on any web server.

## Examples

- **[Drugbank 3D](http://doc.gdb.tools/faerun-python/example3d)**
- **[Drugbank 2D](http://doc.gdb.tools/faerun-python/example2d)**

Furthermore, the documentation of [tmap](https://github.com/reymond-group/tmap) provides a wide range of examples of Faerun in use. See [here](http://tmap.gdb.tools/#ex-nips).

```Python
import numpy as np
from faerun import Faerun

faerun = Faerun(view='free')

t = np.linspace(0, 12.0, 326)
s = np.sin(np.pi * t)
c = np.cos(np.pi * t)

faerun.add_scatter('my_scatter',  { 'x': t, 'y': s, 'z': c, 'c': t / max(t) })
faerun.plot()
```

The code above writes two files to the current directory: `index.html` and `data.js`. These files can be used locally or be moved to a (even minimalistic) web server.

## TODO

- [ ] Add the abilty to draw shapes as well as colours
- [x] Make output templatable

## Documentation
