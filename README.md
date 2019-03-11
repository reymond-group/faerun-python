# Faerun (Python)
Faerun (Python) is based on the [Lore.js](https://github.com/reymond-group/lore) 3D WebGL engine for interactive big data rendering and the [FUn](http://doc.gdb.tools/fun/) project. It facilitates the creation of interactive (2D and 3D) HTML plots of chemical data (or chemical spaces). Molecular structures are rendered using [SmilesDrawer](https://github.com/reymond-group/smilesDrawer).
 
**Associated Publication**: https://academic.oup.com/bioinformatics/article/34/8/1433/4657075

<img alt="Faerun Python" src="http://doc.gdb.tools/faerun-python/intro.png"></img>

## Installation
```Bash
pip install faerun
```

## Examples
- **[Drugbank 3D](http://doc.gdb.tools/faerun-python/example3d)**
- **[Drugbank 2D](http://doc.gdb.tools/faerun-python/example2d)**

The code of the examples shown above for creating interactive 2D and 3D maps from Drugbank can be found in the examples directory. Following, a simple [example](http://doc.gdb.tools/faerun-python/example) of plotting any data:
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
```Python
Faerun(title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', view='free', shader='circle')
```
| Parameter | Default | Description |
|---|---|---|
| title | `'python-faerun'` | The title of the HTML document. |
| clear_color | `'#111111'` | The clear colour,  or background colour is used to clear the canvas after each rendering step. |
| coords | `True` | Whether or not to draw the coordinate axes. |
| coords_color | `'#888888'` | The colour used to draw the coordinate axes. |
| coords_box | `False` | Whether or not to show an encosing box as part of the coordinates. |
| view | `'free'` | The view mode. Available options: `free`, `front`, `back`, `left`, `right`, `bottom`, `top` |

```Python
Faerun.add_scatter(self, name, data, mapping={'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 's': 's', 'labels': 'labels'},
                   colormap='plasma', shader='sphere', point_scale=1.0, max_point_size=100, fog_intensity=0.0, interactive=True)
```
| Parameter | Default | Description |
|---|---|---|
| name | | The name of the plot (has to be unique, if another plot with the same name is added, the existing one will be overwritten). |
| data | | A `dict` or a Pandas `DataFrame` containing the data. |
| mapping | `{'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 's': 's', 'labels': 'labels'}` | The mapping from the `dict` or `DataFrame` to the plot attributes. |
| colormap | `'plasma'` | The colour map to be used. Valid values are [matplotlib colormap names](https://matplotlib.org/examples/color/colormaps_reference.html). |
| shader | `circle` | The name of the shader used to draw the points. Available options: `circle`, `smoothCircle`, `sphere` |
| point_scale | `1.0` | The scale of the points, which is also the radius for raycaster intersections. |
| max_point_size | `100` | The maximum size of a point when zooming in. |
| fog_intensity | `0.0` | The intensity of the fog (points further away fade to the background colour). |
| interactive | `True` | Whether the points are interactive (can be hovered). |
, shader='circle'
```Python
Faerun.add_tree(self, name, data, mapping={'form': 'form', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'},
                color='#666666', colormap='plasma', fog_intensity=0.0, point_helper=None)
```
| Parameter | Default | Description |
|---|---|---|
| name | | The name of the plot (has to be unique, if another plot with the same name is added, the existing one will be overwritten). |
| data | | A `dict` or a Pandas `DataFrame` containing the data. |
| mapping | `{'form': 'form', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 's': 's', 'labels': 'labels'}` | The mapping from the `dict` or `DataFrame` to the plot attributes. |
| color | `'#666666'` | The default colour used when no colour values are supplied. |
| colormap | `'plasma'` | The colour map to be used. Valid values are [matplotlib colormap names](https://matplotlib.org/examples/color/colormaps_reference.html). |
| fog_intensity | `0.0` | The intensity of the fog (points further away fade to the background colour). |
| point_helper | `None` | Using coordinates from a point helper (specified by name) via indices. |

```Python
Faerun.plot(file_name='index', path='./', template='default')
```
| Parameter | Default | Description |
|---|---|---|
| file_name | `'index'` | The file name that is given to both the html and js file. |
| path | `'./'` | The path to which the HTML and data files will be written. |
| template | `'default'` | The HTML template to use. Currently the following templates are available: `'default'`, `'url_image'`, and `'smiles'` |
