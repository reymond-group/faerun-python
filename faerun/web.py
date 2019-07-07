"""
web.py
====================================
An utility module containing all that's needed to host faerun data visualizations.
"""
import os
import pickle
import sys
from typing import Callable, IO

import cherrypy
import numpy as np
import ujson

import faerun

# def index_file(path, out_path):
#     """Create an index for the faerun data file to provide quick access to labels

#     Arguments:
#         path (:obj:`str`): Path of the input faerun data file
#         out_path (:obj:`str`): Path of the output index file

#     Returns:
#         list: The in memory index
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
    print(value)
    return ujson.dumps(value).encode('utf8')


class FaerunWeb():
    """ A cherrypy controller class for hosting fearun visualizations """

    def __init__(self, path: str, label_type: str = 'smiles', theme: str = 'light',
                 label_formatter: Callable[[str, int, str], str] = None,
                 link_formatter: Callable[[str, int, str], str] = None,
                 info: str = None, legend: str = False, legend_title: str ='Legend',
                 view: str = 'front', search_index: int = 1):
        """The constructor for the Faerun web server.
        
        Arguments:
            path (:obj:`str`) -- The path to the faerun data file
        
        Keyword Arguments:
            label_type (:obj:`str`): The type of the labels
            theme (:obj:`str`): The theme to use in the front-end
            label_formatter (:obj:`Callable[[str, int, str], str]`): A function used for formatting labels
            link_formatter (:obj:`Callable[[str, int, str], str]`): A function used for formatting links
            info (:obj:`str`): A string containing markdown content that is shown as an info in the visualization
            legend (:obj:`bool`): Whether or not to show the legend
            legend_title (:obj:`str`): The title of the legend
            view (:obj:`str`): The view type ('front', 'back', 'top', 'bottom', 'right', 'left', or 'free')
            search_index (:obj:`int`): The index in the label values that is used for searching
        """
        if not os.path.isfile(path):
            print('File not found: ' + path)
            sys.exit(1)

        if label_formatter is None:
            label_formatter = lambda label, index, name: label.split('__')[0]

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
        self.search_index = search_index

        for name in self.data:
            if self.data[name]['type'] != 'scatter':
                continue

            # This is currently implemented for two values:
            # e.g. smiles and id
            # seperated by __ in the label field
            self.ids[name] = []

            if isinstance(self.data[name]['labels'][0], str) and '__' in self.data[name]['labels'][0]:
                for _, label in enumerate(self.data[name]['labels']):
                    vals = label.split('__')
                    self.ids[name].append(vals[1].lower())
            else:
                for _, label in enumerate(self.data[name]['labels']):
                    self.ids[name].append(str(label).lower())


    @cherrypy.expose
    def index(self, **params) -> IO:
        """GET the HTML file

        Returns:
            FileType: The HTML file
        """
        return open(faerun.get_asset('index_static.html'))

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out(handler=json_handler)
    @cherrypy.tools.json_in()
    def get_meta(self) -> dict:
        """Get the meta data for the fearun visualization (layers, ...).

        Returns:
            dict: A dict containing the meta information
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
    def get_values(self) -> bytes:
        """Get one set of coordinates or colors (x, y, z, r, g, b) for a faerun layer.

        Returns:
            bytes: An array of values encoded as bytes
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
    def get_label(self) -> dict:
        """Gets the label of a data point based on the layer name and data point index.

        Returns:
            dict: A dict containing the formatted label and link
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
    def get_index(self) -> list:
        """Get the indices of one or more data point based their labels and layer name.

        Returns:
            list: A list of label - index pairs
        """
        input_json = cherrypy.request.json
        labels = input_json['label']
        name = input_json['name']

        labels = str(labels).upper().strip()

        results = []
        for label in labels.split(','):
            label = label.strip().lower()
            try:
                results.append([label, [i for i, v in enumerate(self.ids[name]) if v == label]])
            except ValueError:
                results.append([label, []])

        return results


def host(path: str, label_type: str = 'smiles', theme: str = 'light',
         label_formatter: Callable[[str, int, str], str] = None,
         link_formatter: Callable[[str, int, str], str] = None,
         info: str = None, legend: bool = False, legend_title: str = 'Legend',
         view: str = 'front', search_index: int = 1):
    """Start a cherrypy server hosting a Faerun visualization.

    Arguments:
        path (:obj:`str`): The path to the fearun data file

    Keyword Arguments:
        label_type (:obj:`str`): The type of the labels
        theme (:obj:`str`): The theme to use in the front-end
        label_formatter (:obj:`Callable[[str, int, str], str]`): A function used for formatting labels
        link_formatter (:obj:`Callable[[str, int, str], str]`): A function used for formatting links
        info (:obj:`str`): A string containing markdown content that is shown as an info in the visualization
        legend (:obj:`bool`): Whether or not to show the legend
        legend_title (:obj:`str`): The title of the legend
        view (:obj:`str`): The view type ('front', 'back', 'top', 'bottom', 'right', 'left', or 'free')
        search_index (:obj:`int`): The index in the label values that is used for searching

    """
    cherrypy.quickstart(FaerunWeb(path, label_type, theme, label_formatter=label_formatter,
                                  link_formatter=link_formatter, info=info, legend=legend,
                                  legend_title=legend_title, view=view, search_index=search_index))
