import os
import jinja2
import numpy as np
import matplotlib.pyplot as plt
from yattag import Doc, indent


class Faerun(object):
    """ The faerun class
    """

    def __init__(self, title='python-faerun', clear_color='#111111', coords=True, coords_color='#888888', coords_box=False, view='free'):
        self.title = title
        self.clear_color = clear_color
        self.coords = coords
        self.coords_color = coords_color
        self.coords_box = False
        self.view = view

        self.trees = {}
        self.trees_data = {}
        self.scatters = {}
        self.scatters_data = {}

    def add_tree(self, name, data, mapping={'form': 'form', 'to': 'to', 'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c'},
                 color='#666666', colormap='plasma', fog_intensity=0.0, point_helper=None):
        
        if point_helper == None and mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        self.trees[name] = {
            'name': name, 'color': color, fog_intensity: 0.0,
            'mapping': mapping, 'colormap': colormap, 'point_helper': point_helper
        }
        self.trees_data[name] = data

    def add_scatter(self, name, data, mapping={'x': 'x', 'y': 'y', 'z': 'z', 'c': 'c', 's': 's', 'labels': 'labels'},
                    colormap='plasma', shader='sphere', point_scale=1.0, max_point_size=100, fog_intensity=0.0, interactive=True):

        if mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        self.scatters[name] = {
            'name': name, 'shader': shader, 
            'point_scale': point_scale, 'max_point_size': max_point_size,
            'fog_intensity': fog_intensity, 'interactive': interactive,
            'mapping': mapping, 'colormap': colormap
        }
        self.scatters_data[name] = data



    def plot(self, file_name='index', path='./'):
        script_path = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(path, file_name + '.html')
        js_path = os.path.join(path, file_name + '.js')
        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))

        model = { 
            'title': self.title,
            'file_name': file_name + '.js',
            'clear_color': self.clear_color,
            'view': self.view,
            'coords': self.coords,
            'coords_color': self.coords_color,
            'coords_box': self.coords_box,
            'tree_helpers': list(self.trees.values()),
            'point_helpers': list(self.scatters.values()) 
        }

        output_text = jenv.get_template('template.j2').render(model)

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
            if self.trees[name].point_helper == None:
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




    def create_data(self):
        s = 750
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

        for name, data in self.trees_data:
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
