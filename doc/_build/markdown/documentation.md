# Documentation

## Faerun


#### class faerun.Faerun(title: str = '', clear_color: str = '#111111', coords: bool = True, coords_color: str = '#888888', coords_box: bool = False, coords_ticks: bool = True, coords_grid: bool = False, coords_tick_count: int = 10, coords_tick_length: float = 2.0, coords_offset: float = 5.0, x_title: str = '', y_title: str = '', show_legend: bool = True, legend_title: str = 'Legend', legend_orientation: str = 'vertical', legend_number_format: str = '{:.2f}', view: str = 'free', scale: float = 750.0, alpha_blending=False, style: Dict[str, Dict[str, Any]] = {})
Creates a faerun object which is an empty plotting surface where
layers such as scatter plots can be added.

Constructor for Faerun.


* **Keyword Arguments**

    * **title** (`str`, optional) – The plot title

    * **clear_color** (`str`, optional) – The background color of the plot

    * **coords** (`bool`, optional) – Show the coordinate axes in the plot

    * **coords_color** (`str`, optional) – The color of the coordinate axes

    * **coords_box** (`bool`, optional) – Show a box around the coordinate axes

    * **coords_tick** (`bool`, optional) – Show ticks on coordinate axes

    * **coords_grid** (`bool`, optional) – Extend ticks to create a grid

    * **coords_tick_count** (`int`, optional) – The number of ticks to display per axis

    * **coords_tick_length** (`float`, optional) – The length of the coordinate ticks

    * **coords_offset** (`float`, optional) – An offset added to the coordinate axes

    * **x_title** (`str`, optional) – The title of the x-axis

    * **y_title** (`str`, optional) – The title of the y-axis

    * **show_legend** (`bool`, optional) – Whether or not to show the legend

    * **legend_title** (`str`, optional) – The legend title

    * **legend_orientation** (`str`, optional) – The orientation of the legend (‘vertical’ or ‘horizontal’)

    * **legend_number_format** (`str`, optional) – A format string applied to the numbers displayed in the legend

    * **view** (`str`, optional) – The view (front, back, top, bottom, left, right, free)

    * **scale** (`float`, optional) – To what size to scale the coordinates (which are normalized)

    * **alpha_blending** (`bool`, optional) – Whether to activate alpha blending (required for smoothCircle shader)

    * **style** (`Dict[str, Dict[str, Any]]`, optional) – The css styles to apply to the HTML elements



#### __init__(title: str = '', clear_color: str = '#111111', coords: bool = True, coords_color: str = '#888888', coords_box: bool = False, coords_ticks: bool = True, coords_grid: bool = False, coords_tick_count: int = 10, coords_tick_length: float = 2.0, coords_offset: float = 5.0, x_title: str = '', y_title: str = '', show_legend: bool = True, legend_title: str = 'Legend', legend_orientation: str = 'vertical', legend_number_format: str = '{:.2f}', view: str = 'free', scale: float = 750.0, alpha_blending=False, style: Dict[str, Dict[str, Any]] = {})
Constructor for Faerun.


* **Keyword Arguments**

    * **title** (`str`, optional) – The plot title

    * **clear_color** (`str`, optional) – The background color of the plot

    * **coords** (`bool`, optional) – Show the coordinate axes in the plot

    * **coords_color** (`str`, optional) – The color of the coordinate axes

    * **coords_box** (`bool`, optional) – Show a box around the coordinate axes

    * **coords_tick** (`bool`, optional) – Show ticks on coordinate axes

    * **coords_grid** (`bool`, optional) – Extend ticks to create a grid

    * **coords_tick_count** (`int`, optional) – The number of ticks to display per axis

    * **coords_tick_length** (`float`, optional) – The length of the coordinate ticks

    * **coords_offset** (`float`, optional) – An offset added to the coordinate axes

    * **x_title** (`str`, optional) – The title of the x-axis

    * **y_title** (`str`, optional) – The title of the y-axis

    * **show_legend** (`bool`, optional) – Whether or not to show the legend

    * **legend_title** (`str`, optional) – The legend title

    * **legend_orientation** (`str`, optional) – The orientation of the legend (‘vertical’ or ‘horizontal’)

    * **legend_number_format** (`str`, optional) – A format string applied to the numbers displayed in the legend

    * **view** (`str`, optional) – The view (front, back, top, bottom, left, right, free)

    * **scale** (`float`, optional) – To what size to scale the coordinates (which are normalized)

    * **alpha_blending** (`bool`, optional) – Whether to activate alpha blending (required for smoothCircle shader)

    * **style** (`Dict[str, Dict[str, Any]]`, optional) – The css styles to apply to the HTML elements



#### add_scatter(name: str, data: Union[dict, pandas.core.frame.DataFrame], mapping: dict = {'c': 'c', 'cs': 'cs', 'labels': 'labels', 's': 's', 'x': 'x', 'y': 'y', 'z': 'z'}, colormap: Union[str, matplotlib.colors.Colormap] = 'plasma', shader: str = 'sphere', point_scale: float = 1.0, max_point_size: float = 100.0, fog_intensity: float = 0.0, saturation_limit: float = 0.2, categorical: bool = False, interactive: bool = True, has_legend: bool = False, legend_title: str = None, legend_labels: dict = None, min_legend_label: Union[str, float] = None, max_legend_label: Union[str, float] = None)
Add a scatter layer to the plot.


* **Parameters**

    * **name** (`str`) – The name of the layer

    * **data** (`dict` or `DataFrame`) – A Python dict or Pandas DataFrame containing the data



* **Keyword Arguments**

    * **mapping** (`dict`, optional) – The keys which contain the data in the input dict or the column names in the pandas `DataFrame`

    * **colormap** (`str` or `Colormap`, optional) – The name of the colormap (can also be a matplotlib Colormap object)

    * **shader** (`str`, optional) – The name of the shader to use for the data point visualization

    * **point_scale** (`float`, optional) – The relative size of the data points

    * **max_point_size** (`int`, optional) – The maximum size of the data points when zooming in

    * **fog_intensity** (`float`, optional) – The intensity of the distance fog

    * **saturation_limit** (`float`, optional) – The minimum saturation to avoid “gray soup”

    * **categorical** (`bool`, optional) – Whether this scatter layer is categorical

    * **interactive** (`bool`, optional) – Whether this scatter layer is interactive

    * **has_legend** (`bool`, optional) – Whether or not to draw a legend

    * **legend_title** (`str`, optional) – The title of the legend

    * **legend_labels** (`dict`, optional) – A dict mapping values to legend labels

    * **min_legend_label** (`Union[str, float]`, option) – The label used for the miminum value in a ranged (non-categorical) legend

    * **max_legend_label** (`Union[str, float]`, option) – The label used for the maximum value in a ranged (non-categorical) legend



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



#### static in_notebook()
Checks whether the code is running in an ipython notebook.


* **Returns**

    Whether the code is running in an ipython notebook



* **Return type**

    `bool`



#### plot(file_name: str = 'index', path: str = './', template: str = 'default')
Plots the data to an HTML / JS file.


* **Keyword Arguments**

    * **file_name** (`str`, optional) – The name of the HTML / JS file

    * **path** (`str`, optional) – The path to which to write the HTML / JS file

    * **template** (`str`, optional) – The name of the template to use


## Web


#### faerun.host(path: str, label_type: str = 'smiles', theme: str = 'light', title: str = 'Faerun', label_formatter: Callable[[str, int, str], str] = None, link_formatter: Callable[[str, int, str], str] = None, info: str = None, legend: bool = False, legend_title: str = 'Legend', view: str = 'front', search_index: int = 1)
Start a cherrypy server hosting a Faerun visualization.


* **Parameters**

    **path** (`str`) – The path to the fearun data file



* **Keyword Arguments**

    * **label_type** (`str`) – The type of the labels

    * **theme** (`str`) – The theme to use in the front-end

    * **title** (`str`) – The title of the HTML document

    * **label_formatter** (`Callable[[str, int, str], str]`) – A function used for formatting labels

    * **link_formatter** (`Callable[[str, int, str], str]`) – A function used for formatting links

    * **info** (`str`) – A string containing markdown content that is shown as an info in the visualization

    * **legend** (`bool`) – Whether or not to show the legend

    * **legend_title** (`str`) – The title of the legend

    * **view** (`str`) – The view type (‘front’, ‘back’, ‘top’, ‘bottom’, ‘right’, ‘left’, or ‘free’)

    * **search_index** (`int`) – The index in the label values that is used for searching
