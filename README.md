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

faerun = Faerun(view='free', shader='circle')

t = np.linspace(0, 12.0, 326)
s = np.sin(np.pi * t)
c = np.cos(np.pi * t)
 
faerun.plot({ 'x': t, 'y': s, 'z': c, 'c': t / max(t) })
```

The code above writes two files to the current directory: `index.html` and `data.js`. These files can be used locally or be moved to a (even minimalistic) web server.

## TODO
- [ ] Add the abilty to draw shapes as well as colours
- [ ] Make output templatable

## Documentation
```Python
Faerun(title='python-faerun', point_size=5, tree_color='#aaaaaa', clear_color='#111111', fog_intensity=2.6, coords=True, coords_color='#888888', view='free', shader='circle')
```
| Parameter | Default | Description |
|---|---|---|
| title | `'python-faerun'` | The title of the HTML document. |
| point_size | `5` | The size of the points. |
| tree_color | `'#aaaaaa'` | Not yet implemented. |
| clear_color | `'#111111'` | The clear colour,  or background colour is used to clear the canvas after each rendering step. |
| fog_intensity | `2.6` | Fog is used to darken / lighten far away points depending on the `clear_color`. This is a visual cue helpful for depth perception in orthogonal projections. |
| coords | `True` | Whether or not to draw the coordinate axes. |
| coords_color | `'#888888'` | The colour used to draw the coordinate axes. |
| view | `'free'` | The view mode. Available options: `free`, `front`, `back`, `left`, `right`, `bottom`, `top` |
| shader | `circle` | The name of the shader used to draw the points. Available options: `circle`, `legacyCircle`, `sphere` |

```Python
Faerun.plot(path, data, x='x', y='y', z='z', c='c', colormap='plasma', smiles='smiles', tree=None)
```
| Parameter | Default | Description |
|---|---|---|
| data | | A `dict` or a Pandas `DataFrame` containing the data. |
| x | `x` | The name of the column containing the x-coordinates. |
| x | `y` | The name of the column containing the y-coordinates. |
| x | `z` | The name of the column containing the z-coordinates. |
| c | `c` | The name of the column containing the values by which the points are coloured. **Has to be normalized between 0.0 and 1.0** |
| colormap | `'plasma'` | The colour map to be used. Valid values are [matplotlib colormap names](https://matplotlib.org/examples/color/colormaps_reference.html). |
| smiles | `smiles` | The name of the column containing the SMILES strings with which the points are annotated. |
| path | `''` | The path to which the HTML and data files will be written. |
| tree | `None` | Not yet implemented. |
