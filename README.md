# Faerun (Python)
Faerun (Python) is based on the [Lore.js](https://github.com/reymond-group/lore) 3D WebGL engine for interactive big data rendering and the [FUn](http://doc.gdb.tools/fun/) project. It facilitates the creation of interactive (2D and 3D) HTML plots of chemical data (or chemical spaces). Molecular structures are rendered using [SmilesDrawer](https://github.com/reymond-group/smilesDrawer).
 
**Associated Publication**: https://academic.oup.com/bioinformatics/article/34/8/1433/4657075

<img alt="Faerun Python" src="http://doc.gdb.tools/faerun-python/intro.png"></img>

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
 
data = { 'x': t, 'y': s, 'z': c, 'c': t / max(t) }

faerun.plot(data)
```

## TODO
- [ ] Add the abilty to draw shapes as well as colours
- [ ] Make output templatable