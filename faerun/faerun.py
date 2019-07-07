"""
faerun.py
====================================
The main module containing the Faerun class. 
"""

import math
import os
from typing import Union

import colour
import jinja2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap
from pandas import DataFrame


class Faerun(object):
    """Creates a faerun object which is an empty plotting surface where
     layers such as scatter plots can be added."""

    def __init__(self, title: str = 'python-faerun', clear_color: str = '#111111', coords: bool = True,
                 coords_color: str = '#888888', coords_box: bool = False, view: str = 'free',
                 scale: float = 750.0, alpha_blending=False):
        """Constructor for Faerun.

        Keyword Arguments:
            title (:obj:`str`, optional): The title of the generated HTML file
            clear_color (:obj:`str`, optional): The background color of the plot
            coords (:obj:`bool`, optional): Show the coordinate axes in the plot
            coords_color (:obj:`str`, optional): The color of the coordinate axes
            coords_box (:obj:`bool`, optional): Show a box around the coordinate axes
            view (:obj:`str`, optional): The view (front, back, top, bottom, left, right, free)
            scale (:obj:`float`, optional): To what size to scale the coordinates (which are normalized)
            alpha_blending (:obj:`bool`, optional): Whether to activate alpha blending (required for smoothCircle shader)
        """
        self.title = title
        self.clear_color = clear_color
        self.coords = coords
        self.coords_color = coords_color
        self.coords_box = coords_box
        self.view = view
        self.scale = scale
        self.alpha_blending = alpha_blending

        self.trees = {}
        self.trees_data = {}
        self.scatters = {}
        self.scatters_data = {}

    def add_tree(self, name: str, data: Union[dict, DataFrame],
                 mapping: dict = {'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'},
                 color: str = '#666666', colormap: Union[str, Colormap] = 'plasma',
                 fog_intensity: float = 0.0, point_helper: str = None):
        """Add a tree layer to the plot.

        Arguments:
            name (:obj:`str`): The name of the layer
            data (:obj:`dict` or :obj:`DataFrame`): A Python dict or Pandas DataFrame containing the data

        Keyword Arguments:
            mapping (:obj:`dict`, optional): The keys which contain the data in the input dict or DataFrame
            color (:obj:`str`, optional): The default color of the tree
            colormap (:obj:`str` or :obj:`Colormap`, optional): The name of the colormap (can also be a matplotlib Colormap object)
            fog_intensity (:obj:`float`, optional): The intensity of the distance fog
            point_helper (:obj:`str`, optional): The name of the scatter layer to associate with this tree layer (the source of the coordinates)
        """
        if point_helper is None and mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        self.trees[name] = {
            'name': name, 'color': color, 'fog_intensity': fog_intensity,
            'mapping': mapping, 'colormap': colormap, 'point_helper': point_helper
        }
        self.trees_data[name] = data

    def add_scatter(self, name: str, data: Union[dict, DataFrame],
                    mapping: dict = {'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 'cs': 'cs', 's': 's', 'labels': 'labels'},
                    colormap: Union[str, Colormap] = 'plasma', shader: str = 'sphere',
                    point_scale: float = 1.0, max_point_size: float = 100.0,
                    fog_intensity: float = 0.0, saturation_limit: float = 0.2, 
                    categorical: bool = False, interactive: bool = True,
                    has_legend: bool = False, legend_title: str = None, legend_labels: dict = None):
        """Add a scatter layer to the plot.

        Arguments:
            name (:obj:`str`): The name of the layer
            data (:obj:`dict` or :obj:`DataFrame`): A Python dict or Pandas DataFrame containing the data

        Keyword Arguments:
            mapping (:obj:`dict`, optional): The keys which contain the data in the input dict or the column names in the pandas :obj:`DataFrame`
            colormap (:obj:`str` or :obj:`Colormap`, optional): The name of the colormap (can also be a matplotlib Colormap object)
            shader (:obj:`str`, optional): The name of the shader to use for the data point visualization
            point_scale (:obj:`float`, optional): The relative size of the data points
            max_point_size (:obj:`int`, optional): -- The maximum size of the data points when zooming in
            fog_intensity (:obj:`float`, optional): -- The intensity of the distance fog
            saturation_limit (:obj:`float`, optional): -- The minimum saturation to avoid "gray soup"
            categorical (:obj:`bool`, optional): -- Whether this scatter layer is categorical
            interactive (:obj:`bool`, optional): -- Whether this scatter layer is interactive
            has_legend (:obj:`bool`, optional): -- Whether or not to draw a legend
            legend_title (:obj:`str`, optional): -- The title of the legend
            legend_labels (:obj:`dict`, optional): -- A dict mapping values to legend labels
        """
        if mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        min_c = float(min(data[mapping['c']]))
        max_c = float(max(data[mapping['c']]))
        len_c = len(data[mapping['c']])

        is_range = False

        if legend_title is None:
            legend_title = name

        # Prepare the legend
        legend = []
        if has_legend:
            legend_values = []
            if categorical:
                if legend_labels:
                    legend_values = legend_labels
                else:
                    legend_values = [(i, str(i))
                                     for i in sorted(set(data['c']))]
            else:
                if legend_labels:
                    legend_labels.reverse()
                    for value, label in legend_labels:
                        legend_values.append(
                            ((value - min_c) / (max_c - min_c), label))
                else:
                    is_range = True
                    for i, val in enumerate(np.linspace(0.0, 1.0, 99)):
                        legend_values.append(
                            (val, str(data['c'][int(math.floor(len_c / 100 * i))])))

            cmap = None
            if isinstance(colormap, str):
                cmap = plt.cm.get_cmap(colormap)
            else:
                cmap = colormap

            for value, label in legend_values:
                legend.append((cmap(value), label))

        # Normalize the data to later get the correct colour maps
        if not categorical:
            data[mapping['c']] = np.array(data[mapping['c']])
            data[mapping['c']] = (data[mapping['c']] - min_c) / (max_c - min_c)

        if mapping['cs'] in data:
            data[mapping['cs']] = np.array(data[mapping['cs']])
            min_cs = min(data[mapping['cs']])
            max_cs = max(data[mapping['cs']])
            # Avoid zero saturation by limiting the lower bound to 0.1
            data[mapping['cs']] = 1.0 - np.maximum(saturation_limit, np.array(
                (data[mapping['cs']] - min_cs) / (max_cs - min_cs)))

        self.scatters[name] = {
            'name': name, 'shader': shader,
            'point_scale': point_scale, 'max_point_size': max_point_size,
            'fog_intensity': fog_intensity, 'interactive': interactive,
            'categorical': categorical, 'mapping': mapping, 'colormap': colormap,
            'has_legend': has_legend, 'legend_title': legend_title,
            'legend': legend, 'is_range': is_range,
            'min_c': min_c, 'max_c': max_c
        }

        self.scatters_data[name] = data

    def plot(self, file_name: str = 'index', path: str = './', template: str = 'default', 
             legend_title: str = 'Legend', legend_orientation: str = 'vertical'):
        """Plots the data to an HTML / JS file.

        Keyword Arguments:
            file_name (:obj:`str`, optional): The name of the HTML / JS file
            path (:obj:`str`, optional): The path to which to write the HTML / JS file
            template (:obj:`str`, optional): The name of the template to use
            legend_title (:obj:`str`, optional): The legend title
            legend_orientation (:obj:`str`, optional): The orientation of the legend ('vertical' or 'horizontal')
        """
        script_path = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(path, file_name + '.html')
        js_path = os.path.join(path, file_name + '.js')
        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))

        has_legend = False

        for _, value in self.scatters.items():
            if value['has_legend']:
                has_legend = True
                break

        model = {
            'title': self.title,
            'file_name': file_name + '.js',
            'clear_color': self.clear_color,
            'view': self.view,
            'coords': self.coords,
            'coords_color': self.coords_color,
            'coords_box': self.coords_box,
            'tree_helpers': list(self.trees.values()),
            'point_helpers': list(self.scatters.values()),
            'has_legend': has_legend,
            'legend_title': legend_title,
            'legend_orientation': legend_orientation,
            'alpha_blending': str(self.alpha_blending).lower()
        }

        output_text = jenv.get_template(
            'template_' + template + '.j2').render(model)

        with open(html_path, "w") as result_file:
            result_file.write(output_text)

        with open(js_path, 'w') as f:
            f.write(self.create_data())

    def get_min_max(self) -> tuple:
        """ Get the minimum an maximum coordinates from this plotter instance

            Returns:
                :obj:`tuple`: The minimum and maximum coordinates
        """

        minimum = float('inf')
        maximum = float('-inf')

        for name, data in self.scatters_data.items():
            mapping = self.scatters[name]['mapping']
            min_x = float('inf')
            min_y = float('inf')
            min_z = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')
            max_z = float('-inf')

            if mapping['x'] in data:
                min_x = min(data[mapping['x']])
                max_x = max(data[mapping['x']])

            if mapping['y'] in data:
                min_y = min(data[mapping['y']])
                max_y = max(data[mapping['y']])

            if mapping['z'] in data:
                min_z = min(data[mapping['z']])
                max_z = max(data[mapping['z']])

            minimum = min(minimum, min([min_x, min_y, min_z]))
            maximum = max(maximum, max([max_x, max_y, max_z]))

        for name, data in self.trees_data.items():
            if self.trees[name]['point_helper'] is None:
                mapping = self.trees[name]['mapping']
                min_x = float('inf')
                min_y = float('inf')
                min_z = float('inf')
                max_x = float('-inf')
                max_y = float('-inf')
                max_z = float('-inf')

                if mapping['x'] in data:
                    min_x = min(data[mapping['x']])
                    max_x = max(data[mapping['x']])

                if mapping['y'] in data:
                    min_y = min(data[mapping['y']])
                    max_y = max(data[mapping['y']])

                if mapping['z'] in data:
                    min_z = min(data[mapping['z']])
                    max_z = max(data[mapping['z']])

                minimum = min(minimum, min([min_x, min_y, min_z]))
                maximum = max(maximum, max([max_x, max_y, max_z]))

        return minimum, maximum

    def create_python_data(self) -> dict:
        """Returns a Python dict containing the data

        Returns:
            :obj:`dict`: The data defined in this Faerun instance
        """
        s = self.scale
        minimum, maximum = self.get_min_max()
        diff = maximum - minimum

        output = {}

        # Create the data for the scatters
        for name, data in self.scatters_data.items():
            mapping = self.scatters[name]['mapping']
            colormap = self.scatters[name]['colormap']

            cmap = None
            if isinstance(colormap, str):
                cmap = plt.cm.get_cmap(colormap)
            else:
                cmap = colormap

            output[name] = {}
            output[name]['meta'] = self.scatters[name]
            output[name]['type'] = 'scatter'

            output[name]['x'] = np.array(
                [s * (x - minimum) / diff for x in data[mapping['x']]], dtype=np.float32)
            output[name]['y'] = np.array(
                [s * (y - minimum) / diff for y in data[mapping['y']]], dtype=np.float32)
            output[name]['z'] = np.array(
                [s * (z - minimum) / diff for z in data[mapping['z']]], dtype=np.float32)

            if mapping['labels'] in data:
                # Make sure that the labels are always strings
                output[name]['labels'] = list(map(str, data[mapping['labels']]))

            if mapping['s'] in data:
                output[name]['s'] = np.array(
                    data[mapping['s']], dtype=np.float32)

            if mapping['c'] in data and mapping['cs'] in data:
                colors = np.array([cmap(x) for x in data[mapping['c']]])

                for i, c in enumerate(colors):
                    hsl = np.array(colour.rgb2hsl(c[:3]))
                    hsl[1] = hsl[1] - hsl[1] * data[mapping['cs']][i]
                    colors[i] = np.append(np.array(colour.hsl2rgb(hsl)), 1.0)

                colors = np.round(colors * 255.0)

                output[name]['r'] = np.array(colors[:, 0], dtype=np.float32)
                output[name]['g'] = np.array(colors[:, 1], dtype=np.float32)
                output[name]['b'] = np.array(colors[:, 2], dtype=np.float32)
            elif mapping['c'] in data:
                colors = np.array([cmap(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output[name]['r'] = np.array(colors[:, 0], dtype=np.float32)
                output[name]['g'] = np.array(colors[:, 1], dtype=np.float32)
                output[name]['b'] = np.array(colors[:, 2], dtype=np.float32)

        for name, data in self.trees_data.items():
            mapping = self.trees[name]['mapping']
            point_helper = self.trees[name]['point_helper']

            output[name] = {}
            output[name]['meta'] = self.trees[name]
            output[name]['type'] = 'tree'

            if point_helper is not None and point_helper in self.scatters_data:
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]['mapping']

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping['from']])):
                    x_t.append(scatter[scatter_mapping['x']]
                               [data[mapping['from']][i]])
                    x_t.append(scatter[scatter_mapping['x']]
                               [data[mapping['to']][i]])
                    y_t.append(scatter[scatter_mapping['y']]
                               [data[mapping['from']][i]])
                    y_t.append(scatter[scatter_mapping['y']]
                               [data[mapping['to']][i]])
                    z_t.append(scatter[scatter_mapping['z']]
                               [data[mapping['from']][i]])
                    z_t.append(scatter[scatter_mapping['z']]
                               [data[mapping['to']][i]])

                output[name]['x'] = np.array(
                    [s * (x - minimum) / diff for x in x_t], dtype=np.float32)
                output[name]['y'] = np.array(
                    [s * (y - minimum) / diff for y in y_t], dtype=np.float32)
                output[name]['z'] = np.array(
                    [s * (z - minimum) / diff for z in z_t], dtype=np.float32)
            else:
                output[name]['x'] = np.array(
                    [s * (x - minimum) / diff for x in data[mapping['x']]], dtype=np.float32)
                output[name]['y'] = np.array(
                    [s * (y - minimum) / diff for y in data[mapping['y']]], dtype=np.float32)
                output[name]['z'] = np.array(
                    [s * (z - minimum) / diff for z in data[mapping['z']]], dtype=np.float32)

            if mapping['c'] in data:
                colormap = self.trees[name]['colormap']
                cmap = None
                if isinstance(colormap, str):
                    cmap = plt.cm.get_cmap(colormap)
                else:
                    cmap = colormap

                colors = np.array([cmap(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output[name]['r'] = np.array(colors[:, 0], dtype=np.float32)
                output[name]['g'] = np.array(colors[:, 1], dtype=np.float32)
                output[name]['b'] = np.array(colors[:, 2], dtype=np.float32)

        return output

    def create_data(self) -> str:
        """Returns a JavaScript string defining a JavaScript object containing the data.

        Returns:
            :obj:`str`: JavaScript code defining an object containing the data
        """
        s = self.scale
        minimum, maximum = self.get_min_max()
        diff = maximum - minimum

        output = 'const data = {\n'

        # Create the data for the scatters
        for name, data in self.scatters_data.items():
            mapping = self.scatters[name]['mapping']
            colormap = self.scatters[name]['colormap']
            cmap = None
            if isinstance(colormap, str):
                cmap = plt.cm.get_cmap(colormap)
            else:
                cmap = colormap

            output += name + ': {\n'
            output += 'x: [' + ','.join(map(str, [round(s * (x - minimum) / diff, 3)
                                                  for x in data[mapping['x']]])) + '],\n'
            output += 'y: [' + ','.join(map(str, [round(s * (y - minimum) / diff, 3)
                                                  for y in data[mapping['y']]])) + '],\n'
            output += 'z: [' + ','.join(map(str, [round(s * (z - minimum) / diff, 3)
                                                  for z in data[mapping['z']]])) + '],\n'

            if mapping['labels'] in data:
                output += 'labels: [' + ','.join('\'{0}\''.format(s)
                                                 for s in data[mapping['labels']]) + '],\n'

            if mapping['s'] in data:
                output += 's: [' + \
                    ','.join(map(str, data[mapping['s']])) + '],\n'

            if mapping['c'] in data and mapping['cs'] in data:
                colors = np.array([cmap(x) for x in data[mapping['c']]])

                for i, c in enumerate(colors):
                    hsl = np.array(colour.rgb2hsl(c[:3]))
                    hsl[1] = hsl[1] - hsl[1] * data[mapping['cs']][i]
                    colors[i] = np.append(np.array(colour.hsl2rgb(hsl)), 1.0)

                colors = np.round(colors * 255.0)

                output += 'r: [' + ','.join(map(str, colors[:, 0])) + '],\n'
                output += 'g: [' + ','.join(map(str, colors[:, 1])) + '],\n'
                output += 'b: [' + ','.join(map(str, colors[:, 2])) + '],\n'
            elif mapping['c'] in data:
                colors = np.array([cmap(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output += 'r: [' + ','.join(map(str, colors[:, 0])) + '],\n'
                output += 'g: [' + ','.join(map(str, colors[:, 1])) + '],\n'
                output += 'b: [' + ','.join(map(str, colors[:, 2])) + '],\n'

            output += '},\n'

        for name, data in self.trees_data.items():
            mapping = self.trees[name]['mapping']
            point_helper = self.trees[name]['point_helper']

            output += name + ': {\n'

            if point_helper is not None and point_helper in self.scatters_data:
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]['mapping']

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping['from']])):
                    x_t.append(scatter[scatter_mapping['x']]
                               [data[mapping['from']][i]])
                    x_t.append(scatter[scatter_mapping['x']]
                               [data[mapping['to']][i]])
                    y_t.append(scatter[scatter_mapping['y']]
                               [data[mapping['from']][i]])
                    y_t.append(scatter[scatter_mapping['y']]
                               [data[mapping['to']][i]])
                    z_t.append(scatter[scatter_mapping['z']]
                               [data[mapping['from']][i]])
                    z_t.append(scatter[scatter_mapping['z']]
                               [data[mapping['to']][i]])

                output += 'x: [' + ','.join(
                    map(str, [round(s * (x - minimum) / diff, 3) for x in x_t])) + '],\n'
                output += 'y: [' + ','.join(
                    map(str, [round(s * (y - minimum) / diff, 3) for y in y_t])) + '],\n'
                output += 'z: [' + ','.join(
                    map(str, [round(s * (z - minimum) / diff, 3) for z in z_t])) + '],\n'
            else:
                output += 'x: [' + ','.join(map(str, [round(s * (x - minimum) / diff, 3)
                                                      for x in data[mapping['x']]])) + '],\n'
                output += 'y: [' + ','.join(map(str, [round(s * (y - minimum) / diff, 3)
                                                      for y in data[mapping['y']]])) + '],\n'
                output += 'z: [' + ','.join(map(str, [round(s * (z - minimum) / diff, 3)
                                                      for z in data[mapping['z']]])) + '],\n'

            if mapping['c'] in data:
                colormap = self.trees[name]['colormap']
                cmap = None
                if isinstance(colormap, str):
                    cmap = plt.cm.get_cmap(colormap)
                else:
                    cmap = colormap

                colors = np.array([cmap(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output += 'r: [' + ','.join(map(str, colors[:, 0])) + '],\n'
                output += 'g: [' + ','.join(map(str, colors[:, 1])) + '],\n'
                output += 'b: [' + ','.join(map(str, colors[:, 2])) + '],\n'

            output += '},\n'

        output += '};\n'

        return output

    @staticmethod
    def discrete_cmap(n_colors: int, base_cmap: str) -> Colormap:
        """Create an N-bin discrete colormap from the specified input map.

        Arguments:
            n_colors (:obj:`int`): The number of discrete colors to generate

        Keyword Arguments:
            base_cmap (:obj:`str`): The colormap on which to base the discrete map

        Returns:
            :obj:`Colormap`: The discrete colormap
        """
        # https://gist.github.com/jakevdp/91077b0cae40f8f8244a
        base = plt.cm.get_cmap(base_cmap)
        color_list = base(np.linspace(0, 1, n_colors))
        cmap_name = base.name + str(n_colors)

        return base.from_list(cmap_name, color_list, n_colors)
