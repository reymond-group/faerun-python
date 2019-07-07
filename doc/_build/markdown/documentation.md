# Documentation

## Faerun


#### class faerun.Faerun(title: str = 'python-faerun', clear_color: str = '#111111', coords: bool = True, coords_color: str = '#888888', coords_box: bool = False, view: str = 'free', scale: float = 750.0)
Creates a faerun object which is an empty plotting surface where
layers such as scatter plots can be added.

Constructor for Faerun.


* **Keyword Arguments**

    * **title** (`str`, optional) – The title of the generated HTML file

    * **clear_color** (`str`, optional) – The background color of the plot

    * **coords** (`bool`, optional) – Show the coordinate axes in the plot

    * **coords_color** (`str`, optional) – The color of the coordinate axes

    * **coords_box** (`bool`, optional) – Show a box around the coordinate axes

    * **view** (`str`, optional) – The view (front, back, top, bottom, left, right, free)

    * **scale** (`float`, optional) – To what size to scale the coordinates (which are normalized)



#### __init__(title: str = 'python-faerun', clear_color: str = '#111111', coords: bool = True, coords_color: str = '#888888', coords_box: bool = False, view: str = 'free', scale: float = 750.0)
Constructor for Faerun.


* **Keyword Arguments**

    * **title** (`str`, optional) – The title of the generated HTML file

    * **clear_color** (`str`, optional) – The background color of the plot

    * **coords** (`bool`, optional) – Show the coordinate axes in the plot

    * **coords_color** (`str`, optional) – The color of the coordinate axes

    * **coords_box** (`bool`, optional) – Show a box around the coordinate axes

    * **view** (`str`, optional) – The view (front, back, top, bottom, left, right, free)

    * **scale** (`float`, optional) – To what size to scale the coordinates (which are normalized)



#### add_scatter(name: str, data: Union[dict, pandas.core.frame.DataFrame], mapping: dict = {'c': 'c', 'cs': 'cs', 'labels': 'labels', 's': 's', 'x': 'x', 'y': 'y', 'z': 'z'}, colormap: Union[str, matplotlib.colors.Colormap] = 'plasma', shader: str = 'sphere', point_scale: float = 1.0, max_point_size: float = 100.0, fog_intensity: float = 0.0, saturation_limit: float = 0.2, categorical: bool = False, interactive: bool = True, has_legend: bool = False, legend_title: str = None, legend_labels: dict = None)
Add a scatter layer to the plot.


* **Parameters**

    * **name** (`str`) – The name of the layer

    * **data** (`dict` or `DataFrame`) – A Python dict or Pandas DataFrame containing the data



* **Keyword Arguments**

    * **mapping** (`dict`, optional) – The keys which contain the data in the input dict or the column names in the pandas `DataFrame`

    * **colormap** (`str` or `Colormap`, optional) – The name of the colormap (can also be a matplotlib Colormap object)

    * **shader** (`str`, optional) – The name of the shader to use for the data point visualization

    * **point_scale** (`float`, optional) – The relative size of the data points

    * **max_point_size** (`int`, optional) – – The maximum size of the data points when zooming in

    * **fog_intensity** (`float`, optional) – – The intensity of the distance fog

    * **saturation_limit** (`float`, optional) – – The minimum saturation to avoid “gray soup”

    * **categorical** (`bool`, optional) – – Whether this scatter layer is categorical

    * **interactive** (`bool`, optional) – – Whether this scatter layer is interactive

    * **has_legend** (`bool`, optional) – – Whether or not to draw a legend

    * **legend_title** (`str`, optional) – – The title of the legend

    * **legend_labels** (`dict`, optional) – – A dict mapping values to legend labels



#### add_tree(name: str, data: Union[dict, pandas.core.frame.DataFrame], mapping: dict = {'c': 'c', 'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z'}, color: str = '#666666', colormap: Union[str, matplotlib.colors.Colormap] = 'plasma', fog_intensity: float = 0.0, point_helper: str = None)
Add a tree layer to the plot.


* **Parameters**

    * **name** (`str`) – The name of the layer

    * **data** (`dict` or `DataFrame`) – A Python dict or Pandas DataFrame containing the data



* **Keyword Arguments**

    * **mapping** (`dict`, optional) – The keys which contain the data in the input dict or DataFrame

    * **color** (`str`, optional) – The default color of the tree

    * **colormap** (`str` or `Colormap`, optional) – The name of the colormap (can also be a matplotlib Colormap object)

    * **fog_intensity** (`float`, optional) – The intensity of the distance fog

    * **point_helper** (`str`, optional) – The name of the scatter layer to associate with this tree layer (the source of the coordinates)



#### create_data()
Returns a JavaScript string defining a JavaScript object containing the data.


* **Returns**

    JavaScript code defining an object containing the data



* **Return type**

    `str`



#### create_python_data()
Returns a Python dict containing the data


* **Returns**

    The data defined in this Faerun instance



* **Return type**

    `dict`



#### static discrete_cmap(n_colors: int, base_cmap: str)
Create an N-bin discrete colormap from the specified input map.


* **Parameters**

    **n_colors** (`int`) – The number of discrete colors to generate



* **Keyword Arguments**

    **base_cmap** (`str`) – The colormap on which to base the discrete map



* **Returns**

    The discrete colormap



* **Return type**

    `Colormap`



#### get_min_max()
Get the minimum an maximum coordinates from this plotter instance


* **Returns**

    The minimum and maximum coordinates



* **Return type**

    `tuple`



#### plot(file_name: str = 'index', path: str = './', template: str = 'default', legend_title: str = 'Legend', legend_orientation: str = 'vertical')
Plots the data to an HTML / JS file.


* **Keyword Arguments**

    * **file_name** (`str`, optional) – The name of the HTML / JS file

    * **path** (`str`, optional) – The path to which to write the HTML / JS file

    * **template** (`str`, optional) – The name of the template to use

    * **legend_title** (`str`, optional) – The legend title

    * **legend_orientation** (`str`, optional) – The orientation of the legend (‘vertical’ or ‘horizontal’)


## Web


#### faerun.host(path: str, label_type: str = 'smiles', theme: str = 'light', label_formatter: Callable[[str, int, str], str] = None, link_formatter: Callable[[str, int, str], str] = None, info: str = None, legend: bool = False, legend_title: str = 'Legend', view: str = 'front', search_index: int = 1)
Start a cherrypy server hosting a Faerun visualization.


* **Parameters**

    **path** (`str`) – The path to the fearun data file



* **Keyword Arguments**

    * **label_type** (`str`) – The type of the labels

    * **theme** (`str`) – The theme to use in the front-end

    * **label_formatter** (`Callable[[str, int, str], str]`) – A function used for formatting labels

    * **link_formatter** (`Callable[[str, int, str], str]`) – A function used for formatting links

    * **info** (`str`) – A string containing markdown content that is shown as an info in the visualization

    * **legend** (`bool`) – Whether or not to show the legend

    * **legend_title** (`str`) – The title of the legend

    * **view** (`str`) – The view type (‘front’, ‘back’, ‘top’, ‘bottom’, ‘right’, ‘left’, or ‘free’)

    * **search_index** (`int`) – The index in the label values that is used for searching
