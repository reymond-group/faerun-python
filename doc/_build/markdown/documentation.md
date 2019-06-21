# Documentation

## Faerun


#### class faerun.Faerun(title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', coords_box=False, view='free', scale=750)
Creates a faerun object which is an empty plotting surface where
layers such as scatter plots can be added.


#### __init__(title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', coords_box=False, view='free', scale=750)
Constructor for Faerun


* **Keyword Arguments**

    * **{str} -- The title of the generated HTML file**** (****default** (*title*) – {‘python-faerun’})

    * **{str} -- The background color of the plot**** (****default** (*clear_color*) – {‘#111111’})

    * **{bool} -- Show the coordinate axes in the plot**** (****default** (*coords*) – {True})

    * **{str} -- The color of the coordinate axes**** (****default** (*coords_color*) – {‘#888888’})

    * **{bool} -- Show a box around the coordinate axes**** (****default** (*coords_box*) – {False})

    * **{str} -- The view** (*view*) – {‘free’})

    * **{int} -- To what size to scale the coordinates** (*scale*) – {750})



#### add_scatter(name, data, mapping={'c': 'c', 'cs': 'cs', 'labels': 'labels', 's': 's', 'x': 'x', 'y': 'y', 'z': 'z'}, colormap='plasma', shader='sphere', point_scale=1.0, max_point_size=100, fog_intensity=0.0, saturation_limit=0.2, categorical=False, interactive=True, has_legend=False, legend_title=None, legend_labels=None)
Add a scatter layer to the plot


* **Parameters**

    * **{str} -- The name of the layer** (*name*) – 

    * **{object} -- A Python dict**** or ****Pandas DataFrame containing the data** (*data*) – 



* **Keyword Arguments**

    * **{dict} -- The keys which contain the data in the input dict**** or ****DataFrame**** (****default** (*mapping*) – {{‘x’: ‘x’, ‘y’: ‘y’, ‘z’: ‘z’, ‘c’: ‘c’, ‘cs’: ‘cs’, ‘s’: ‘s’, ‘labels’: ‘labels’}})

    * **{str} -- The name of the colormap** (*colormap*) – {‘plasma’})

    * **{str} -- The name of the shader to use for the data point visualization**** (****default** (*shader*) – {‘sphere’})

    * **{float} -- The relative size of the data points**** (****default** (*point_scale*) – {1.0})

    * **{int} -- The maximum size of the data points when zooming in**** (****default** (*max_point_size*) – {100})

    * **{float} -- The intensity of the distance fog**** (****default** (*fog_intensity*) – {0.0})

    * **{float} -- The minimum saturation to avoid "gray soup"**** (****default** (*saturation_limit*) – {0.2})

    * **{bool} -- Whether this scatter layer is categorical**** (****default** (*categorical*) – {False})

    * **{bool} -- Whether this scatter layer is interactive**** (****default** (*interactive*) – {True})

    * **{bool} -- Whether**** or ****not to draw a legend**** (****default** (*has_legend*) – {False})

    * **{str} -- The title of the legend**** (****default** (*legend_title*) – {None})

    * **{dict} -- A dict mapping values to legend labels**** (****default** (*legend_labels*) – {None})



#### add_tree(name, data, mapping={'c': 'c', 'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z'}, color='#666666', colormap='plasma', fog_intensity=0.0, point_helper=None)
Add a tree layer to the plot


* **Parameters**

    * **{str} -- The name of the layer** (*name*) – 

    * **{object} -- A Python  dict**** or ****Pandas DataFrame containing the data** (*data*) – 



* **Keyword Arguments**

    * **{dict} -- The keys which contain the data in the input dict**** or ****DataFrame**** (****default** (*mapping*) – {{‘from’: ‘from’, ‘to’: ‘to’, ‘x’: ‘x’, ‘y’: ‘y’, ‘z’: ‘z’, ‘c’: ‘c’}})

    * **{str} -- The default color of the tree**** (****default** (*color*) – {‘#666666’})

    * **{str} -- The name of the colormap** (*colormap*) – {‘plasma’})

    * **{float} -- The intensity of the distance fog**** (****default** (*fog_intensity*) – {0.0})

    * **{str} -- The name of the scatter layer to associate with this tree layer** (*point_helper*) – {None})



#### create_data()
Returns a JavaScript string defining a JavaScript object containing the data


* **Returns**

    str – JavaScript code defining an object containing the data



#### create_python_data()
Returns a Python dict containing the data


* **Returns**

    dict – The data defined in this Faerun instance



#### static discrete_cmap(n_colors, base_cmap=None)
Create an N-bin discrete colormap from the specified input map


* **Parameters**

    **{int} -- The number of discrete colors to generate** (*n_colors*) – 



* **Keyword Arguments**

    **{Colormap} -- The colormap on which to base tje discrete map**** (****default** (*base_cmap*) – {None})



* **Returns**

    Colormap – The discrete colormap



#### get_min_max()
Get the minimum an maximum coordinates from this plotter instance


* **Returns**

    tuple – The minimum and maximum coordinates



#### plot(file_name='index', path='./', template='default', legend_title='Legend', legend_orientation='vertical')
Plots the data to an HTML / JS file


* **Keyword Arguments**

    * **{str} -- The name of the HTML / JS file**** (****default** (*file_name*) – {‘index’})

    * **{str} -- The path to which to write the HTML / JS file**** (****default** (*path*) – {‘./’})

    * **{str} -- The name of the template to use.**** (****default** (*template*) – {‘default’})

    * **{str} -- The legend title**** (****default** (*legend_title*) – {‘Legend’})

    * **{str} -- The orientation of the legend** (*legend_orientation*) – {‘vertical’})


## Web


#### faerun.web.host(path, label_type='smiles', theme='light', label_formatter=None, link_formatter=None, info=None, legend=False, legend_title='Legend', view='front', search_index=1)
Start a cherrypy server hosting a Faerun visualization


* **Parameters**

    **{str} -- The path to the fearun data file** (*path*) – 



* **Keyword Arguments**

    * **{str} -- The type of the labels**** (****default** (*label_type*) – {‘smiles’})

    * **{str} -- The theme to use in the front-end**** (****default** (*theme*) – {‘light’})

    * **{FunctionType} -- A function used for formatting labels**** (****default** (*label_formatter*) – {None})

    * **{FunctionType} -- A function used for formatting links**** (****default** (*link_formatter*) – {None})

    * **{str} -- A string containing markdown content that is shown as an info in the visualization**** (****default** (*info*) – {None})

    * **{bool} -- Whether**** or ****not to show the legend**** (****default** (*legend*) – {False})

    * **{str} -- The title of the legend**** (****default** (*legend_title*) – {‘Legend’})

    * **{str} -- The view type** (*view*) – {‘front’})

    * **{int} -- The index in the label values that is used for searching**** (****default** (*search_index*) – {1})
