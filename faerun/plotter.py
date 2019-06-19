import os
import jinja2
import math
import colour

import numpy as np
import matplotlib.pyplot as plt


class Faerun(object):
    """ The main class for generating Faerun visualizations
    """

    def __init__(self, title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', coords_box=False, view='free', scale=750):
        """Constructor for Faerun

        Keyword Arguments:
            title {str} -- The title of the generated HTML file (default: {'python-faerun'})
            clear_color {str} -- The background color of the plot (default: {'#111111'})
            coords {bool} -- Show the coordinate axes in the plot (default: {True})
            coords_color {str} -- The color of the coordinate axes (default: {'#888888'})
            coords_box {bool} -- Show a box around the coordinate axes (default: {False})
            view {str} -- The view (top, left, free ...) (default: {'free'})
            scale {int} -- To what size to scale the coordinates (which are normalized) (default: {750})
        """
        self.title = title
        self.clear_color = clear_color
        self.coords = coords
        self.coords_color = coords_color
        self.coords_box = coords_box
        self.view = view
        self.scale = scale

        self.trees = {}
        self.trees_data = {}
        self.scatters = {}
        self.scatters_data = {}

    def add_tree(self, name, data,
                 mapping={'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'},
                 color='#666666', colormap='plasma', fog_intensity=0.0, point_helper=None):
        """Add a tree layer to the plot

        Arguments:
            name {str} -- The name of the layer
            data {object} -- A Python  dict or Pandas DataFrame containing the data

        Keyword Arguments:
            mapping {dict} -- The keys which contain the data in the input dict or DataFrame (default: {{'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'}})
            color {str} -- The default color of the tree (default: {'#666666'})
            colormap {str} -- The name of the colormap (can also be a matplotlib Colormap object) (default: {'plasma'})
            fog_intensity {float} -- The intensity of the distance fog (default: {0.0})
            point_helper {str} -- The name of the scatter layer to associate with this tree layer (the source of the coordinates) (default: {None})
        """
        if point_helper is None and mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        self.trees[name] = {
            'name': name, 'color': color, 'fog_intensity': fog_intensity,
            'mapping': mapping, 'colormap': colormap, 'point_helper': point_helper
        }
        self.trees_data[name] = data

    def add_scatter(self, name, data,
                    mapping={'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 'cs': 'cs', 's': 's', 'labels': 'labels'},
                    colormap='plasma', shader='sphere', point_scale=1.0, max_point_size=100, 
                    fog_intensity=0.0, saturation_limit=0.2, categorical=False, interactive=True, 
                    has_legend=False, legend_title=None, legend_labels=None):
        """Add a scatter layer to the plot

        Arguments:
            name {str} -- The name of the layer
            data {object} -- A Python dict or Pandas DataFrame containing the data

        Keyword Arguments:
            mapping {dict} -- The keys which contain the data in the input dict or DataFrame (default: {{'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 'cs': 'cs', 's': 's', 'labels': 'labels'}})
            colormap {str} -- The name of the colormap (can also be a matplotlib Colormap object) (default: {'plasma'})
            shader {str} -- The name of the shader to use for the data point visualization (default: {'sphere'})
            point_scale {float} -- The relative size of the data points (default: {1.0})
            max_point_size {int} -- The maximum size of the data points when zooming in (default: {100})
            fog_intensity {float} -- The intensity of the distance fog (default: {0.0})
            saturation_limit {float} -- The minimum saturation to avoid "gray soup" (default: {0.2})
            categorical {bool} -- Whether this scatter layer is categorical (default: {False})
            interactive {bool} -- Whether this scatter layer is interactive (default: {True})
            has_legend {bool} -- Whether or not to draw a legend (default: {False})
            legend_title {str} -- The title of the legend (default: {None})
            legend_labels {dict} -- A dict mapping values to legend labels (default: {None})
        """
        if mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        min_c = min(data[mapping['c']])
        max_c = max(data[mapping['c']])
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

    def plot(self, file_name='index', path='./', template='default', legend_title='Legend', 
             legend_orientation='vertical'):
        """Plots the data to an HTML / JS file

        Keyword Arguments:
            file_name {str} -- The name of the HTML / JS file (default: {'index'})
            path {str} -- The path to which to write the HTML / JS file (default: {'./'})
            template {str} -- The name of the template to use (default: {'default'})
            legend_title {str} -- The legend title (default: {'Legend'})
            legend_orientation {str} -- The orientation of the legend (vertical or horizontal) (default: {'vertical'})
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
            'legend_orientation': legend_orientation
        }

        output_text = jenv.get_template(
            'template_' + template + '.j2').render(model)

        with open(html_path, "w") as result_file:
            result_file.write(output_text)

        with open(js_path, 'w') as f:
            f.write(self.create_data())

    def get_min_max(self):
        """Get the minimum an maximum coordinates from this plotter instance

        Returns:
            tuple -- The minimum and maximum coordinates
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

    def create_python_data(self):
        """Returns a Python dict containing the data

        Returns:
            dict -- The data defined in this Faerun instance
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
                output[name]['labels'] = data[mapping['labels']]

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

    def create_data(self):
        """Returns a JavaScript string defining a JavaScript object containing the data

        Returns:
            str -- JavaScript code defining an object containing the data
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
    def discrete_cmap(n_colors, base_cmap=None):
        """Create an N-bin discrete colormap from the specified input map

        Arguments:
            n_colors {int} -- The number of discrete colors to generate
        
        Keyword Arguments:
            base_cmap {Colormap} -- The colormap on which to base tje discrete map (default: {None})

        Returns:
            Colormap -- The discrete colormap
        """
        # https://gist.github.com/jakevdp/91077b0cae40f8f8244a
        base = plt.cm.get_cmap(base_cmap)
        color_list = base(np.linspace(0, 1, n_colors))
        cmap_name = base.name + str(n_colors)

        return base.from_list(cmap_name, color_list, n_colors)
