import os
import jinja2
import math

import numpy as np
import matplotlib.pyplot as plt

class Faerun(object):
    """ The faerun class
    """

    def __init__(self, title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', coords_box=False, view='free', scale=750):
        self.title = title
        self.clear_color = clear_color
        self.coords = coords
        self.coords_color = coords_color
        self.coords_box = False
        self.view = view
        self.scale = scale

        self.trees = {}
        self.trees_data = {}
        self.scatters = {}
        self.scatters_data = {}

    def add_tree(self, name, data, mapping={'from': 'from', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'},
                 color='#666666', colormap='plasma', fog_intensity=0.0, point_helper=None):
        
        if point_helper == None and mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        self.trees[name] = {
            'name': name, 'color': color, 'fog_intensity': 0.0,
            'mapping': mapping, 'colormap': colormap, 'point_helper': point_helper
        }
        self.trees_data[name] = data

    def add_scatter(self, name, data, mapping={'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 's': 's', 'labels': 'labels'},
                    colormap='plasma', shader='sphere', point_scale=1.0, max_point_size=100, fog_intensity=0.0, 
                    categorical=False, interactive=True, has_legend=False,  legend_title=None, legend_labels=None):

        if mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        min_c = min(data['c'])
        max_c = max(data['c'])
        len_c = len(data['c'])

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
                    legend_values = [(i, str(i)) for i in sorted(set(data['c']))]
            else:
                if legend_labels:
                    legend_labels.reverse()
                    for value, label in legend_labels:
                        legend_values.append(( (value - min_c) / (max_c - min_c), label ))     
                else:
                    is_range = True
                    for i, val in enumerate(np.linspace(0.0, 1.0, 99)):
                        legend_values.append((val, str(data['c'][int(math.floor(len_c / 100 * i))])))
            
            for value, label in legend_values:
                legend.append((plt.cm.get_cmap(colormap)(value), label))
            


        # Normalize the data to later get the correct colour maps
        if not categorical:
            data['c'] = np.array(data['c'])
            data['c'] = (data['c'] - min_c) / (max_c - min_c)

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

    def plot(self, file_name='index', path='./', template='default', legend_title='Legend'):
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
            'legend_title': legend_title
        }

        output_text = jenv.get_template('template_' + template + '.j2').render(model)

        with open(html_path, "w") as result_file:
            result_file.write(output_text)

        with open(js_path, 'w') as f:
            f.write(self.create_data())



    def get_min_max(self):
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
            if self.trees[name]['point_helper'] == None:
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
        s = self.scale
        minimum, maximum = self.get_min_max()
        diff = maximum - minimum

        output = {}
        
        # Create the data for the scatters
        for name, data in self.scatters_data.items(): 
            mapping = self.scatters[name]['mapping']
            colormap = self.scatters[name]['colormap']
            
            output[name] = {}

            output[name]['x'] = np.array([s * (x - minimum) / diff for x in data[mapping['x']]], dtype=np.float32)
            output[name]['y'] = np.array([s * (y - minimum) / diff for y in data[mapping['y']]], dtype=np.float32)
            output[name]['z'] = np.array([s * (z - minimum) / diff for z in data[mapping['z']]], dtype=np.float32)
                
            
            if mapping['labels'] in data:
                output[name]['labels'] = data[mapping['labels']]

            if mapping['s'] in data:
                output[name]['s'] = np.array(data[mapping['s']], dtype=np.float32)
            
            if mapping['c'] in data:
                colors = np.array([plt.cm.get_cmap(colormap)(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output[name]['r'] = np.array(colors[:,0], dtype=np.float32)
                output[name]['g'] = np.array(colors[:,1], dtype=np.float32)
                output[name]['b'] = np.array(colors[:,2], dtype=np.float32)

        for name, data in self.trees_data.items():
            mapping = self.trees[name]['mapping']
            point_helper = self.trees[name]['point_helper']

            output[name] = {}

            if point_helper != None and point_helper in self.scatters_data:  
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]['mapping']

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping['from']])):
                    x_t.append(scatter[scatter_mapping['x']][data[mapping['from']][i]])
                    x_t.append(scatter[scatter_mapping['x']][data[mapping['to']][i]])
                    y_t.append(scatter[scatter_mapping['y']][data[mapping['from']][i]])
                    y_t.append(scatter[scatter_mapping['y']][data[mapping['to']][i]])
                    z_t.append(scatter[scatter_mapping['z']][data[mapping['from']][i]])
                    z_t.append(scatter[scatter_mapping['z']][data[mapping['to']][i]])

                output[name]['x'] = np.array([s * (x - minimum) / diff for x in x_t], dtype=np.float32)
                output[name]['y'] = np.array([s * (y - minimum) / diff for y in y_t], dtype=np.float32)
                output[name]['z'] = np.array([s * (z - minimum) / diff for z in z_t], dtype=np.float32)
            else:
                output[name]['x'] = np.array([s * (x - minimum) / diff for x in data[mapping['x']]], dtype=np.float32)
                output[name]['y'] = np.array([s * (y - minimum) / diff for y in data[mapping['y']]], dtype=np.float32)
                output[name]['z'] = np.array([s * (z - minimum) / diff for z in data[mapping['z']]], dtype=np.float32)

            if mapping['c'] in data:
                colormap = self.trees[name]['colormap']
                colors = np.array([plt.cm.get_cmap(colormap)(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output[name]['r'] = np.array(colors[:,0], dtype=np.float32)
                output[name]['g'] = np.array(colors[:,1], dtype=np.float32)
                output[name]['b'] = np.array(colors[:,2], dtype=np.float32)

        return output

    def create_data(self):
        s = self.scale
        minimum, maximum = self.get_min_max()
        diff = maximum - minimum

        output = 'const data = {\n'
        
        # Create the data for the scatters
        for name, data in self.scatters_data.items(): 
            mapping = self.scatters[name]['mapping']
            colormap = self.scatters[name]['colormap']

            output += name + ': {\n'

            output += 'x: [' + ','.join(map(str, [round(s * (x - minimum) / diff, 3) for x in data[mapping['x']]])) + '],\n'
            output += 'y: [' + ','.join(map(str, [round(s * (y - minimum) / diff, 3) for y in data[mapping['y']]])) + '],\n'
            output += 'z: [' + ','.join(map(str, [round(s * (z - minimum) / diff, 3) for z in data[mapping['z']]])) + '],\n'
                
            
            if mapping['labels'] in data:
                output += 'labels: [' + ','.join('\'{0}\''.format(s) for s in data[mapping['labels']]) + '],\n'

            if mapping['s'] in data:
                output += 's: [' + ','.join(map(str, data[mapping['s']])) + '],\n'
            
            if mapping['c'] in data:
                colors = np.array([plt.cm.get_cmap(colormap)(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output += 'r: [' + ','.join(map(str, colors[:,0])) + '],\n'
                output += 'g: [' + ','.join(map(str, colors[:,1])) + '],\n'
                output += 'b: [' + ','.join(map(str, colors[:,2])) + '],\n'
            
            output += '},\n'

        for name, data in self.trees_data.items():
            mapping = self.trees[name]['mapping']
            point_helper = self.trees[name]['point_helper']

            output += name + ': {\n'

            if point_helper != None and point_helper in self.scatters_data:  
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]['mapping']

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping['from']])):
                    x_t.append(scatter[scatter_mapping['x']][data[mapping['from']][i]])
                    x_t.append(scatter[scatter_mapping['x']][data[mapping['to']][i]])
                    y_t.append(scatter[scatter_mapping['y']][data[mapping['from']][i]])
                    y_t.append(scatter[scatter_mapping['y']][data[mapping['to']][i]])
                    z_t.append(scatter[scatter_mapping['z']][data[mapping['from']][i]])
                    z_t.append(scatter[scatter_mapping['z']][data[mapping['to']][i]])

                output += 'x: [' + ','.join(map(str, [round(s * (x - minimum) / diff, 3) for x in x_t])) + '],\n'
                output += 'y: [' + ','.join(map(str, [round(s * (y - minimum) / diff, 3) for y in y_t])) + '],\n'
                output += 'z: [' + ','.join(map(str, [round(s * (z - minimum) / diff, 3) for z in z_t])) + '],\n'
            else:
                output += 'x: [' + ','.join(map(str, [round(s * (x - minimum) / diff, 3) for x in data[mapping['x']]])) + '],\n'
                output += 'y: [' + ','.join(map(str, [round(s * (y - minimum) / diff, 3) for y in data[mapping['y']]])) + '],\n'
                output += 'z: [' + ','.join(map(str, [round(s * (z - minimum) / diff, 3) for z in data[mapping['z']]])) + '],\n'

            if mapping['c'] in data:
                colormap = self.trees[name]['colormap']
                colors = np.array([plt.cm.get_cmap(colormap)(x) for x in data[mapping['c']]])
                colors = np.round(colors * 255.0)
                output += 'r: [' + ','.join(map(str, colors[:,0])) + '],\n'
                output += 'g: [' + ','.join(map(str, colors[:,1])) + '],\n'
                output += 'b: [' + ','.join(map(str, colors[:,2])) + '],\n'
                
            output += '},\n'

        output += '};\n'

        return output
