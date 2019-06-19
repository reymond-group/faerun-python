""" An utility module containing all that's needed to host faerun data visualizations """
import os
import pickle
import sys

import cherrypy
import faerun
import numpy as np
import ujson


# def index_file(path, out_path):
#     """Create an index for the faerun data file to provide quick access to labels

#     Arguments:
#         path {str} -- Path of the input faerun data file
#         out_path {str} -- Path of the output index file

#     Returns:
#         list -- The in memory index
#     """
#     indices = []
#     with open(out_path, 'w+') as f_out:
#         with open(path, 'r') as f_in:
#             for line in iter(f_in.readline, ''):
#                 pos = f_in.tell()
#                 length = len(line)
#                 start = pos - length
#                 indices.append(start)
#                 indices.append(length)
#                 f_out.write(str(start) + ',' + str(length))

#     return indices

def json_handler(*args, **kwargs):
    """ The default cherrypy json encoder seems to be extremely slow... """
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return ujson.dumps(value).encode('utf8')


class FaerunWeb():
    """ A cherrypy controller class for hosting fearun visualizations """

    def __init__(self, path, label_type='smiles', theme='light', label_formatter=None, link_formatter=None,
                 info=None, legend=False, legend_title='Legend', view='front'):
        if not os.path.isfile(path):
            print('File not found: ' + path)
            sys.exit(1)

        if label_formatter is None:
            label_formatter = lambda label, index, name: label

        if link_formatter is None:
            link_formatter = lambda label, index, name: ''

        self.label_type = label_type
        self.theme = theme
        self.data = pickle.load(open(path, 'rb'))
        self.ids = {}
        self.link_formatter = link_formatter
        self.label_formatter = label_formatter
        self.info = info
        self.legend = legend
        self.legend_title = legend_title
        self.view = view

        for name in self.data:
            if self.data[name]['type'] != 'scatter':
                continue

            # This is currently implemented for two values:
            # e.g. smiles and id
            # seperated by __ in the label field
            self.ids[name] = []

            if '__' in self.data[name]['labels'][0]:
                for _, label in enumerate(self.data[name]['labels']):
                    vals = label.split('__')
                    self.ids[name].append(vals[1].lower())
            else:
                for _, label in enumerate(self.data[name]['labels']):
                    self.ids[name].append(label.lower())

    @cherrypy.expose
    def index(self, **params):
        """GET the HTML file

        Returns:
            FileType -- The HTML file
        """
        return open(faerun.get_asset('index_static.html'))

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(handler=json_handler)
    @cherrypy.tools.json_in()
    def get_meta(self):
        """Get the meta data for the fearun visualization (layers, ...)

        Returns:
            dict -- A dict containing the meta information
        """
        meta = {}
        meta['label_type'] = self.label_type
        meta['theme'] = self.theme
        meta['info'] = self.info
        meta['legend'] = self.legend
        meta['legend_title'] = self.legend_title
        meta['view'] = self.view

        for name in self.data:
            data_type = self.data[name]['type']
            if data_type not in meta:
                meta[data_type] = {}
            meta[data_type][name] = self.data[name]['meta']
        return meta

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    # @cherrypy.tools.json_out(handler=json_handler)
    @cherrypy.tools.json_in()
    def get_values(self):
        """Get one set of coordinates or colors (x, y, z, r, g, b) for a faerun layer

        Returns:
            bytes -- An array of values encoded as bytes
        """
        input_json = cherrypy.request.json
        name = input_json['name']
        coord = input_json['coord']
        dtype = input_json['dtype']

        if dtype == 'float32':
            dtype = np.float32
        elif dtype == 'uint8':
            dtype = np.uint8

        return bytes(np.array(self.data[name][coord].tolist(), dtype=dtype))

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(handler=json_handler)
    @cherrypy.tools.json_in()
    def get_label(self):
        """Gets the label of a data point based on the layer name and data point index

        Returns:
            dict -- A dict containing the formatted label and link
        """
        input_json = cherrypy.request.json
        index = input_json['id']
        name = input_json['name']
        label = self.data[name]['labels'][index]

        return {
            'label': self.label_formatter(label, index, name),
            'link': self.link_formatter(label, index, name)
        }

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(handler=json_handler)
    @cherrypy.tools.json_in()
    def get_index(self):
        """Get the indices of one or more data point based their labels and layer name

        Returns:
            list -- A list of label - index pairs
        """
        input_json = cherrypy.request.json
        labels = input_json['label']
        name = input_json['name']

        labels = str(labels).upper().strip()

        results = []
        for label in labels.split(','):
            label = label.strip().lower()
            try:
                results.append([label, self.ids[name].index(label)])
            except ValueError:
                results.append([label, -1])

        return results


def host(path, label_type='smiles', theme='light', label_formatter=None, link_formatter=None, 
         info=None, legend=False, legend_title='Legend', view='front'):
    """Start a cherrypy server hosting a faerun visualization

    Arguments:
        path {str} -- The path to the fearun data file

    Keyword Arguments:
        label_type {str} -- The type of the labels (default: {'smiles'})
        theme {str} -- The theme to use in the front-end (default: {'light'})
        label_formatter {FunctionType} -- A function used for formatting labels (default: {None})
        link_formatter {FunctionType} -- A function used for formatting links (default: {None})
    """
    cherrypy.quickstart(FaerunWeb(path, label_type, theme, label_formatter=label_formatter,
                                  link_formatter=link_formatter, info=info, legend=legend,
                                  legend_title=legend_title, view=view))
