"""
faerun.py
====================================
The main module containing the Faerun class.
"""

import math
import os
import copy
from typing import Union, Dict, Any, List, Tuple
from collections.abc import Iterable

import colour
import jinja2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap
from pandas import DataFrame

try:
    from IPython.display import display, IFrame, FileLink
except Exception:
    pass


class Faerun(object):
    """Creates a faerun object which is an empty plotting surface where
     layers such as scatter plots can be added."""

    def __init__(
        self,
        title: str = "",
        clear_color: str = "#111111",
        coords: bool = True,
        coords_color: str = "#888888",
        coords_box: bool = False,
        coords_ticks: bool = True,
        coords_grid: bool = False,
        coords_tick_count: int = 10,
        coords_tick_length: float = 2.0,
        coords_offset: float = 5.0,
        x_title: str = "",
        y_title: str = "",
        show_legend: bool = True,
        legend_title: str = "Legend",
        legend_orientation: str = "vertical",
        legend_number_format: str = "{:.2f}",
        view: str = "free",
        scale: float = 750.0,
        alpha_blending=False,
        anti_aliasing=True,
        style: Dict[str, Dict[str, Any]] = {},
        impress: str = None
    ):
        """Constructor for Faerun.

        Keyword Arguments:
            title (:obj:`str`, optional): The plot title
            clear_color (:obj:`str`, optional): The background color of the plot
            coords (:obj:`bool`, optional): Show the coordinate axes in the plot
            coords_color (:obj:`str`, optional): The color of the coordinate axes
            coords_box (:obj:`bool`, optional): Show a box around the coordinate axes
            coords_tick (:obj:`bool`, optional): Show ticks on coordinate axes
            coords_grid (:obj:`bool`, optional): Extend ticks to create a grid
            coords_tick_count (:obj:`int`, optional): The number of ticks to display per axis
            coords_tick_length (:obj:`float`, optional): The length of the coordinate ticks
            coords_offset (:obj:`float`, optional): An offset added to the coordinate axes
            x_title (:obj:`str`, optional): The title of the x-axis
            y_title (:obj:`str`, optional): The title of the y-axis
            show_legend (:obj:`bool`, optional): Whether or not to show the legend
            legend_title (:obj:`str`, optional): The legend title
            legend_orientation (:obj:`str`, optional): The orientation of the legend ('vertical' or 'horizontal')
            legend_number_format (:obj:`str`, optional): A format string applied to the numbers displayed in the legend
            view (:obj:`str`, optional): The view (front, back, top, bottom, left, right, free)
            scale (:obj:`float`, optional): To what size to scale the coordinates (which are normalized)
            alpha_blending (:obj:`bool`, optional): Whether to activate alpha blending (required for smoothCircle shader)
            anti_aliasing (:obj:`bool`, optional): Whether to activate anti-aliasing. Might improve quality at the cost of (substantial) rendering performance
            style (:obj:`Dict[str, Dict[str, Any]]`, optional): The css styles to apply to the HTML elements
            impress (:obj:`str`, optional): A short message that is shown on the HTML page
        """
        self.title = title
        self.clear_color = clear_color
        self.coords = coords
        self.coords_color = coords_color
        self.coords_box = coords_box
        self.coords_ticks = coords_ticks
        self.coords_grid = coords_grid
        self.coords_tick_count = coords_tick_count
        self.coords_tick_length = coords_tick_length
        self.coords_offset = coords_offset
        self.x_title = x_title
        self.y_title = y_title
        self.show_legend = show_legend
        self.legend_title = legend_title
        self.legend_orientation = legend_orientation
        self.legend_number_format = legend_number_format
        self.view = view
        self.scale = scale
        self.alpha_blending = alpha_blending
        self.anti_aliasing = anti_aliasing
        self.style = style
        self.impress = impress

        self.trees = {}
        self.trees_data = {}
        self.scatters = {}
        self.scatters_data = {}

        # Defining the default style (css values)
        default_style = {
            "legend": {
                "bottom": "10px",
                "right": "10px",
                "padding": "10px",
                "border": "1px solid #262626",
                "border-radius": "2px",
                "background-color": "#111111",
                "filter": "drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5))",
                "color": "#eeeeee",
                "font-family": "'Open Sans'",
            },
            "selected": {
                "bottom": "10px",
                "left": "10px",
                "padding": "0px",
                "border": "1px solid #262626",
                "border-radius": "2px",
                "background-color": "#111111",
                "filter": "drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5))",
                "color": "#eeeeee",
                "font-family": "'Open Sans'",
            },
            "controls": {
                "top": "10px",
                "right": "10px",
                "padding": "2px",
                "border": "1px solid #262626",
                "border-radius": "2px",
                "background-color": "#111111",
                "filter": "drop-shadow(0px 0px 10px rgba(0, 0, 0, 0.5))",
                "color": "#eeeeee",
                "font-family": "'Open Sans'",
            },
            "title": {
                "padding-bottom": "20px",
                "font-size": "1.0em",
                "color": "#888888",
                "font-family": "'Open Sans'",
            },
            "x-axis": {
                "padding-top": "20px",
                "font-size": "0.7em",
                "color": "#888888",
                "font-family": "'Open Sans'",
            },
            "y-axis": {
                "padding-bottom": "20px",
                "font-size": "0.7em",
                "color": "#888888",
                "font-family": "'Open Sans'",
                "transform": "rotate(-90deg)",
            },
            "color-box": {"width": "15px", "height": "15px", "border": "solid 0px"},
            "color-stripe": {"width": "15px", "height": "1px", "border": "solid 0px"},
            "color-stripe": {"width": "15px", "height": "1px", "border": "solid 0px"},
            "crosshair": {"background-color": "#fff"}
        }

        for key, _ in default_style.items():
            if key in self.style:
                default_style[key].update(self.style[key])

        self.style = default_style

    def add_tree(
        self,
        name: str,
        data: Union[dict, DataFrame],
        mapping: dict = {
            "from": "from",
            "to": "to",
            "x": "x",
            "y": "y",
            "z": "z",
            "c": "c",
        },
        color: str = "#666666",
        colormap: Union[str, Colormap] = "plasma",
        fog_intensity: float = 0.0,
        point_helper: str = None,
    ):
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
        if point_helper is None and mapping["z"] not in data:
            data[mapping["z"]] = [0] * len(data[mapping["x"]])

        self.trees[name] = {
            "name": name,
            "color": color,
            "fog_intensity": fog_intensity,
            "mapping": mapping,
            "colormap": colormap,
            "point_helper": point_helper,
        }
        self.trees_data[name] = data

    def add_scatter(
        self,
        name: str,
        data: Union[Dict, DataFrame],
        mapping: Dict = {
            "x": "x",
            "y": "y",
            "z": "z",
            "c": "c",
            "cs": "cs",
            "s": "s",
            "labels": "labels",
        },
        colormap: Union[str, Colormap, List[str], List[Colormap]] = "plasma",
        shader: str = "sphere",
        point_scale: float = 1.0,
        max_point_size: float = 100.0,
        fog_intensity: float = 0.0,
        saturation_limit: Union[float, List[float]] = 0.2,
        categorical: Union[bool, List[bool]] = False,
        interactive: bool = True,
        has_legend: bool = False,
        legend_title: Union[str, List[str]] = None,
        legend_labels: Union[Dict, List[Dict]] = None,
        min_legend_label: Union[str, float, List[str], List[float]] = None,
        max_legend_label: Union[str, float, List[str], List[float]] = None,
        series_title: Union[str, List[str]] = None,
        ondblclick: Union[str, List[str]] = None,
        selected_labels: Union[List, List[List]] = None,
        label_index: Union[int, List[int]] = 0,
        title_index: Union[int, List[int]] = 0,
    ):
        """Add a scatter layer to the plot.

        Arguments:
            name (:obj:`str`): The name of the layer
            data (:obj:`dict` or :obj:`DataFrame`): A Python dict or Pandas DataFrame containing the data

        Keyword Arguments:
            mapping (:obj:`dict`, optional): The keys which contain the data in the input dict or the column names in the pandas :obj:`DataFrame`
            colormap (:obj:`str`, :obj:`Colormap`, :obj:`List[str]`, or :obj:`List[Colormap]` optional): The name of the colormap (can also be a matplotlib Colormap object). A list when visualizing multiple series
            shader (:obj:`str`, optional): The name of the shader to use for the data point visualization
            point_scale (:obj:`float`, optional): The relative size of the data points
            max_point_size (:obj:`int`, optional): The maximum size of the data points when zooming in
            fog_intensity (:obj:`float`, optional): The intensity of the distance fog
            saturation_limit (:obj:`float` or :obj:`List[float]`, optional): The minimum saturation to avoid "gray soup". A list when visualizing multiple series
            categorical (:obj:`bool` or :obj:`List[bool]`, optional): Whether this scatter layer is categorical. A list when visualizing multiple series
            interactive (:obj:`bool`, optional): Whether this scatter layer is interactive
            has_legend (:obj:`bool`, optional): Whether or not to draw a legend
            legend_title (:obj:`str` or :obj:`List[str]`, optional): The title of the legend. A list when visualizing multiple series
            legend_labels (:obj:`Dict` or :obj:`List[Dict]`, optional): A dict mapping values to legend labels. A list when visualizing multiple series
            min_legend_label (:obj:`str`, :obj:`float`, :obj:`List[str]` or :obj:`List[float]`, optional): The label used for the miminum value in a ranged (non-categorical) legend. A list when visualizing multiple series
            max_legend_label (:obj:`str`, :obj:`float`, :obj:`List[str]` or :obj:`List[float]`, optional): The label used for the maximum value in a ranged (non-categorical) legend. A list when visualizing multiple series
            series_title (:obj:`str` or :obj:`List[str]`, optional): The name of the series (used when multiple properites supplied). A list when visualizing multiple series
            ondblclick (:obj:`str` or :obj:`List[str]`, optional): A JavaScript snippet that is executed on double-clicking on a data point. A list when visualizing multiple series
            selected_labels: (:obj:`Dict` or :obj:`List[Dict]`, optional): A list of label values to show in the selected box. A list when visualizing multiple series
            label_index: (:obj:`int` or :obj:`List[int]`, optional): The index of the label value to use as the actual label (when __ is used to specify multiple values). A list when visualizing multiple series
            title_index: (:obj:`int` or :obj:`List[int]`, optional): The index of the label value to use as the selected title (when __ is used to specify multiple values). A list when visualizing multiple series
        """
        if mapping["z"] not in data:
            data[mapping["z"]] = [0] * len(data[mapping["x"]])

        if "pandas" in type(data).__module__:
            data = data.to_dict("list")

        data_c = data[mapping["c"]]
        data_cs = data[mapping["c"]] if mapping["cs"] in data else None

        # Check whether the color ("c") are strings
        if type(data_c[0]) is str:
            raise ValueError('Strings are not valid values for "c".')

        # In case there are multiple series defined
        n_series = 1
        if isinstance(data_c[0], Iterable):
            n_series = len(data_c)
        else:
            data_c = [data_c]

        if data_cs is not None and not isinstance(data_cs[0], Iterable):
            data_cs = [data_cs]

        # Make everything a list that isn't one (or a tuple)
        colormap = Faerun.make_list(colormap)
        saturation_limit = Faerun.make_list(saturation_limit)
        categorical = Faerun.make_list(categorical)
        legend_title = Faerun.make_list(legend_title)
        legend_labels = Faerun.make_list(legend_labels, make_list_list=True)
        min_legend_label = Faerun.make_list(min_legend_label)
        max_legend_label = Faerun.make_list(max_legend_label)
        series_title = Faerun.make_list(series_title)
        ondblclick = Faerun.make_list(ondblclick)
        selected_labels = Faerun.make_list(selected_labels, make_list_list=True)
        label_index = Faerun.make_list(label_index)
        title_index = Faerun.make_list(title_index)

        # If any argument list is shorter than the number of series,
        # repeat the last element
        colormap = Faerun.expand_list(colormap, n_series)
        saturation_limit = Faerun.expand_list(saturation_limit, n_series)
        categorical = Faerun.expand_list(categorical, n_series)
        legend_title = Faerun.expand_list(legend_title, n_series, with_none=True)
        legend_labels = Faerun.expand_list(legend_labels, n_series, with_none=True)
        min_legend_label = Faerun.expand_list(
            min_legend_label, n_series, with_none=True
        )
        max_legend_label = Faerun.expand_list(
            max_legend_label, n_series, with_none=True
        )
        series_title = Faerun.expand_list(series_title, n_series, with_value="Series")
        ondblclick = Faerun.expand_list(ondblclick, n_series, with_none=True)
        selected_labels = Faerun.expand_list(selected_labels, n_series)
        label_index = Faerun.expand_list(label_index, n_series)
        title_index = Faerun.expand_list(title_index, n_series)

        # # The c and cs values in the data are a special case, as they should
        # # never be expanded
        # if type(data[mapping["c"]][0]) is not list and prop_len > 1:
        #     prop_len = 1
        # elif:
        #     prop_len = len(data[mapping["c"]])

        legend = [None] * n_series
        is_range = [None] * n_series
        min_c = [None] * n_series
        max_c = [None] * n_series

        for s in range(n_series):
            min_c[s] = float(min(data_c[s]))
            max_c[s] = float(max(data_c[s]))
            len_c = len(data_c[s])

            if min_legend_label[s] is None:
                min_legend_label[s] = min_c[s]

            if max_legend_label[s] is None:
                max_legend_label[s] = max_c[s]

            is_range[s] = False

            if legend_title[s] is None:
                legend_title[s] = name

            # Prepare the legend
            legend[s] = []
            if has_legend:
                legend_values = []
                if categorical[s]:
                    if legend_labels[s]:
                        legend_values = legend_labels[s]
                    else:
                        legend_values = [(i, str(i)) for i in sorted(set(data_c[s]))]
                else:
                    if legend_labels[s]:
                        legend_labels[s].reverse()
                        for value, label in legend_labels[s]:
                            legend_values.append(
                                [(value - min_c[s]) / (max_c[s] - min_c[s]), label]
                            )
                    else:
                        is_range[s] = True
                        for i, val in enumerate(np.linspace(1.0, 0.0, 99)):
                            legend_values.append(
                                [val, str(data_c[s][int(math.floor(len_c / 100 * i))])]
                            )

                cmap = None
                if isinstance(colormap[s], str):
                    cmap = plt.cm.get_cmap(colormap[s])
                else:
                    cmap = colormap[s]

                for value, label in legend_values:
                    legend[s].append([list(cmap(value)), label])

            # Normalize the data to later get the correct colour maps
            if not categorical[s]:
                data_c[s] = np.array(data_c[s])
                data_c[s] = (data_c[s] - min_c[s]) / (max_c[s] - min_c[s])

            if mapping["cs"] in data and len(data_cs) > s:
                data_cs[s] = np.array(data_cs[s])
                min_cs = min(data_cs[s])
                max_cs = max(data_cs[s])
                # Avoid zero saturation by limiting the lower bound to 0.1

                data_cs[s] = 1.0 - np.maximum(
                    saturation_limit[s],
                    np.array((data_cs[s] - min_cs) / (max_cs - min_cs)),
                )

            # Format numbers if parameters are indeed numbers
            if isinstance(min_legend_label[s], (int, float)):
                min_legend_label[s] = self.legend_number_format.format(
                    min_legend_label[s]
                )

            if isinstance(max_legend_label[s], (int, float)):
                max_legend_label[s] = self.legend_number_format.format(
                    max_legend_label[s]
                )

        data[mapping["c"]] = data_c
        if data_cs:
            data[mapping["cs"]] = data_cs

        self.scatters[name] = {
            "name": name,
            "shader": shader,
            "point_scale": point_scale,
            "max_point_size": max_point_size,
            "fog_intensity": fog_intensity,
            "interactive": interactive,
            "categorical": categorical,
            "mapping": mapping,
            "colormap": colormap,
            "has_legend": has_legend,
            "legend_title": legend_title,
            "legend": legend,
            "is_range": is_range,
            "min_c": min_c,
            "max_c": max_c,
            "min_legend_label": min_legend_label,
            "max_legend_label": max_legend_label,
            "series_title": series_title,
            "ondblclick": ondblclick,
            "selected_labels": selected_labels,
            "label_index": label_index,
            "title_index": title_index,
        }

        self.scatters_data[name] = data

    def plot(
        self,
        file_name: str = "index",
        path: str = "./",
        template: str = "default",
        notebook_height: int = 500,
    ):
        """Plots the data to an HTML / JS file.

        Keyword Arguments:
            file_name (:obj:`str`, optional): The name of the HTML / JS file
            path (:obj:`str`, optional): The path to which to write the HTML / JS file
            template (:obj:`str`, optional): The name or path of the template to use
            notebook_height: (:obj`int`, optional): The height of the plot when displayed in a jupyter notebook
        """
        self.notebook_height = notebook_height

        script_path = os.path.dirname(os.path.abspath(__file__))
        if template in ["default", "smiles", "url_image"]:
            template = "template_" + template + ".j2"
        else:
            script_path = os.path.dirname(template)
 
        html_path = os.path.join(path, file_name + ".html")
        js_path = os.path.join(path, file_name + ".js")
        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))

        has_legend = False

        for _, value in self.scatters.items():
            if value["has_legend"]:
                has_legend = True
                break

        if not self.show_legend:
            has_legend = False

        # Drop colormaps before passing them to the document, as they are
        # not JSON serializable.
        trees_copy = copy.deepcopy(self.trees)
        scatters_copy = copy.deepcopy(self.scatters)

        for key, _ in trees_copy.items():
            del trees_copy[key]["colormap"]

        for key, _ in scatters_copy.items():
            del scatters_copy[key]["colormap"]

        model = {
            "title": self.title,
            "file_name": file_name + ".js",
            "clear_color": self.clear_color,
            "view": self.view,
            "coords": str(self.coords).lower(),
            "coords_color": self.coords_color,
            "coords_box": str(self.coords_box).lower(),
            "coords_ticks": str(self.coords_ticks).lower(),
            "coords_grid": str(self.coords_grid).lower(),
            "coords_tick_count": self.coords_tick_count,
            "coords_tick_length": self.coords_tick_length,
            "coords_offset": self.coords_offset,
            "x_title": self.x_title,
            "y_title": self.y_title,
            "tree_helpers": list(trees_copy.values()),
            "point_helpers": list(scatters_copy.values()),
            "has_legend": str(has_legend).lower(),
            "legend_title": self.legend_title,
            "legend_orientation": self.legend_orientation,
            "alpha_blending": str(self.alpha_blending).lower(),
            "anti_aliasing": str(self.anti_aliasing).lower(),
            "style": self.style,
            "impress": self.impress,
            "in_notebook": Faerun.in_notebook(),
        }

        if Faerun.in_notebook():
            model["data"] = self.create_data()
        else:
            with open(js_path, "w") as f:
                f.write(self.create_data())

        output_text = jenv.get_template(template).render(model)

        with open(html_path, "w") as result_file:
            result_file.write(output_text)

        if Faerun.in_notebook():
            display(IFrame(html_path, width="100%", height=self.notebook_height))
            display(FileLink(html_path))

    def get_min_max(self) -> tuple:
        """ Get the minimum an maximum coordinates from this plotter instance

            Returns:
                :obj:`tuple`: The minimum and maximum coordinates
        """

        minimum = float("inf")
        maximum = float("-inf")

        for name, data in self.scatters_data.items():
            mapping = self.scatters[name]["mapping"]
            min_x = float("inf")
            min_y = float("inf")
            min_z = float("inf")
            max_x = float("-inf")
            max_y = float("-inf")
            max_z = float("-inf")

            if mapping["x"] in data:
                min_x = min(data[mapping["x"]])
                max_x = max(data[mapping["x"]])

            if mapping["y"] in data:
                min_y = min(data[mapping["y"]])
                max_y = max(data[mapping["y"]])

            if mapping["z"] in data:
                min_z = min(data[mapping["z"]])
                max_z = max(data[mapping["z"]])

            minimum = min(minimum, min([min_x, min_y, min_z]))
            maximum = max(maximum, max([max_x, max_y, max_z]))

        for name, data in self.trees_data.items():
            if self.trees[name]["point_helper"] is None:
                mapping = self.trees[name]["mapping"]
                min_x = float("inf")
                min_y = float("inf")
                min_z = float("inf")
                max_x = float("-inf")
                max_y = float("-inf")
                max_z = float("-inf")

                if mapping["x"] in data:
                    min_x = min(data[mapping["x"]])
                    max_x = max(data[mapping["x"]])

                if mapping["y"] in data:
                    min_y = min(data[mapping["y"]])
                    max_y = max(data[mapping["y"]])

                if mapping["z"] in data:
                    min_z = min(data[mapping["z"]])
                    max_z = max(data[mapping["z"]])

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
            mapping = self.scatters[name]["mapping"]
            colormaps = self.scatters[name]["colormap"]
            cmaps = [None] * len(colormaps)

            for i, colormap in enumerate(colormaps):
                if isinstance(colormap, str):
                    cmaps[i] = plt.cm.get_cmap(colormap)
                else:
                    cmaps[i] = colormap

            output[name] = {}
            output[name]["meta"] = self.scatters[name]
            output[name]["type"] = "scatter"

            output[name]["x"] = np.array(
                [s * (x - minimum) / diff for x in data[mapping["x"]]], dtype=np.float32
            )
            output[name]["y"] = np.array(
                [s * (y - minimum) / diff for y in data[mapping["y"]]], dtype=np.float32
            )
            output[name]["z"] = np.array(
                [s * (z - minimum) / diff for z in data[mapping["z"]]], dtype=np.float32
            )

            if mapping["labels"] in data:
                # Make sure that the labels are always strings
                output[name]["labels"] = list(map(str, data[mapping["labels"]]))

            if mapping["s"] in data:
                output[name]["s"] = np.array(data[mapping["s"]], dtype=np.float32)

            output[name]["colors"] = [{}] * len(data[mapping["c"]])
            for s in range(len(data[mapping["c"]])):
                if mapping["cs"] in data:
                    colors = np.array([cmaps[s](x) for x in data[mapping["c"]][s]])

                    for i, c in enumerate(colors):
                        hsl = np.array(colour.rgb2hsl(c[:3]))
                        hsl[1] = hsl[1] - hsl[1] * data[mapping["cs"]][s][i]
                        colors[i] = np.append(np.array(colour.hsl2rgb(hsl)), 1.0)

                    colors = np.round(colors * 255.0)

                    output[name]["colors"][s]["r"] = np.array(
                        colors[:, 0], dtype=np.float32
                    )
                    output[name]["colors"][s]["g"] = np.array(
                        colors[:, 1], dtype=np.float32
                    )
                    output[name]["colors"][s]["b"] = np.array(
                        colors[:, 2], dtype=np.float32
                    )
                else:
                    colors = np.array([cmaps[s](x) for x in data[mapping["c"]][s]])
                    colors = np.round(colors * 255.0)
                    output[name]["colors"][s]["r"] = np.array(
                        colors[:, 0], dtype=np.float32
                    )
                    output[name]["colors"][s]["g"] = np.array(
                        colors[:, 1], dtype=np.float32
                    )
                    output[name]["colors"][s]["b"] = np.array(
                        colors[:, 2], dtype=np.float32
                    )

        for name, data in self.trees_data.items():
            mapping = self.trees[name]["mapping"]
            point_helper = self.trees[name]["point_helper"]

            output[name] = {}
            output[name]["meta"] = self.trees[name]
            output[name]["type"] = "tree"

            if point_helper is not None and point_helper in self.scatters_data:
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]["mapping"]

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping["from"]])):
                    x_t.append(scatter[scatter_mapping["x"]][data[mapping["from"]][i]])
                    x_t.append(scatter[scatter_mapping["x"]][data[mapping["to"]][i]])
                    y_t.append(scatter[scatter_mapping["y"]][data[mapping["from"]][i]])
                    y_t.append(scatter[scatter_mapping["y"]][data[mapping["to"]][i]])
                    z_t.append(scatter[scatter_mapping["z"]][data[mapping["from"]][i]])
                    z_t.append(scatter[scatter_mapping["z"]][data[mapping["to"]][i]])

                output[name]["x"] = np.array(
                    [s * (x - minimum) / diff for x in x_t], dtype=np.float32
                )
                output[name]["y"] = np.array(
                    [s * (y - minimum) / diff for y in y_t], dtype=np.float32
                )
                output[name]["z"] = np.array(
                    [s * (z - minimum) / diff for z in z_t], dtype=np.float32
                )
            else:
                output[name]["x"] = np.array(
                    [s * (x - minimum) / diff for x in data[mapping["x"]]],
                    dtype=np.float32,
                )
                output[name]["y"] = np.array(
                    [s * (y - minimum) / diff for y in data[mapping["y"]]],
                    dtype=np.float32,
                )
                output[name]["z"] = np.array(
                    [s * (z - minimum) / diff for z in data[mapping["z"]]],
                    dtype=np.float32,
                )

            if mapping["c"] in data:
                colormap = self.trees[name]["colormap"]
                cmap = None
                if isinstance(colormap, str):
                    cmap = plt.cm.get_cmap(colormap)
                else:
                    cmap = colormap

                colors = np.array([cmap(x) for x in data[mapping["c"]]])
                colors = np.round(colors * 255.0)
                output[name]["r"] = np.array(colors[:, 0], dtype=np.float32)
                output[name]["g"] = np.array(colors[:, 1], dtype=np.float32)
                output[name]["b"] = np.array(colors[:, 2], dtype=np.float32)

        return output

    def create_data(self) -> str:
        """Returns a JavaScript string defining a JavaScript object containing the data.

        Returns:
            :obj:`str`: JavaScript code defining an object containing the data
        """
        s = self.scale
        mini, maxi = self.get_min_max()
        diff = maxi - mini

        output = "const data = {\n"

        # Create the data for the scatters
        # TODO: If it's not interactive, labels shouldn't be exported.
        for name, data in self.scatters_data.items():
            mapping = self.scatters[name]["mapping"]
            colormaps = self.scatters[name]["colormap"]
            cmaps = [None] * len(colormaps)

            for i, colormap in enumerate(colormaps):
                if isinstance(colormap, str):
                    cmaps[i] = plt.cm.get_cmap(colormap)
                else:
                    cmaps[i] = colormap

            output += name + ": {\n"
            x_norm = [round(s * (x - mini) / diff, 3) for x in data[mapping["x"]]]
            output += "x: [" + ",".join(map(str, x_norm)) + "],\n"

            y_norm = [round(s * (y - mini) / diff, 3) for y in data[mapping["y"]]]
            output += "y: [" + ",".join(map(str, y_norm)) + "],\n"

            z_norm = [round(s * (z - mini) / diff, 3) for z in data[mapping["z"]]]
            output += "z: [" + ",".join(map(str, z_norm)) + "],\n"

            if mapping["labels"] in data:
                fmt_labels = ["'{0}'".format(s) for s in data[mapping["labels"]]]
                output += "labels: [" + ",".join(fmt_labels) + "],\n"

            if mapping["s"] in data:
                output += "s: [" + ",".join(map(str, data[mapping["s"]])) + "],\n"

            output += "colors: [\n"
            for series in range(len(data[mapping["c"]])):
                output += "{\n"
                if mapping["cs"] in data:
                    colors = np.array(
                        [cmaps[series](x) for x in data[mapping["c"]][series]]
                    )

                    for i, c in enumerate(colors):
                        hsl = np.array(colour.rgb2hsl(c[:3]))
                        hsl[1] = hsl[1] - hsl[1] * data[mapping["cs"]][series][i]
                        colors[i] = np.append(np.array(colour.hsl2rgb(hsl)), 1.0)

                    colors = np.round(colors * 255.0)

                    output += "r: [" + ",".join(map(str, map(int, colors[:, 0]))) + "],\n"
                    output += "g: [" + ",".join(map(str, map(int, colors[:, 1]))) + "],\n"
                    output += "b: [" + ",".join(map(str, map(int, colors[:, 2]))) + "],\n"
                elif mapping["c"] in data:
                    colors = np.array(
                        [cmaps[series](x) for x in data[mapping["c"]][series]]
                    )
                    colors = np.round(colors * 255.0)
                    output += "r: [" + ",".join(map(str, map(int, colors[:, 0]))) + "],\n"
                    output += "g: [" + ",".join(map(str, map(int, colors[:, 1]))) + "],\n"
                    output += "b: [" + ",".join(map(str, map(int, colors[:, 2]))) + "],\n"
                output += "},\n"

            output += "]"
            output += "},\n"

        for name, data in self.trees_data.items():
            mapping = self.trees[name]["mapping"]
            point_helper = self.trees[name]["point_helper"]

            output += name + ": {\n"

            if point_helper is not None and point_helper in self.scatters_data:
                scatter = self.scatters_data[point_helper]
                scatter_mapping = self.scatters[point_helper]["mapping"]

                x_t = []
                y_t = []
                z_t = []

                for i in range(len(data[mapping["from"]])):
                    x_t.append(scatter[scatter_mapping["x"]][data[mapping["from"]][i]])
                    x_t.append(scatter[scatter_mapping["x"]][data[mapping["to"]][i]])
                    y_t.append(scatter[scatter_mapping["y"]][data[mapping["from"]][i]])
                    y_t.append(scatter[scatter_mapping["y"]][data[mapping["to"]][i]])
                    z_t.append(scatter[scatter_mapping["z"]][data[mapping["from"]][i]])
                    z_t.append(scatter[scatter_mapping["z"]][data[mapping["to"]][i]])

                x_norm = [round(s * (x - mini) / diff, 3) for x in x_t]
                output += f"x: [" + ",".join(map(str, x_norm)) + "],\n"

                y_norm = [round(s * (y - mini) / diff, 3) for y in y_t]
                output += "y: [" + ",".join(map(str, y_norm)) + "],\n"

                z_norm = [round(s * (z - mini) / diff, 3) for z in z_t]
                output += "z: [" + ",".join(map(str, z_norm)) + "],\n"
            else:
                x_norm = [round(s * (x - mini) / diff, 3) for x in data[mapping["x"]]]
                output += "x: [" + ",".join(map(str, x_norm)) + "],\n"

                y_norm = [round(s * (y - mini) / diff, 3) for y in data[mapping["y"]]]
                output += "y: [" + ",".join(map(str, y_norm)) + "],\n"

                z_norm = [round(s * (z - mini) / diff, 3) for z in data[mapping["z"]]]
                output += "z: [" + ",".join(map(str, z_norm)) + "],\n"

            if mapping["c"] in data:
                colormap = self.trees[name]["colormap"]
                cmap = None
                if isinstance(colormap, str):
                    cmap = plt.cm.get_cmap(colormap)
                else:
                    cmap = colormap

                colors = np.array([cmap(x) for x in data[mapping["c"]]])
                colors = np.round(colors * 255.0)
                output += "r: [" + ",".join(map(str, colors[:, 0])) + "],\n"
                output += "g: [" + ",".join(map(str, colors[:, 1])) + "],\n"
                output += "b: [" + ",".join(map(str, colors[:, 2])) + "],\n"

            output += "},\n"

        output += "};\n"

        return output

    @staticmethod
    def make_list(obj: Any, make_list_list: bool = False) -> List:
        """ If an object isn't a list, it is added to one and returned,
        otherwise, the list is returned.

        Arguments:
            obj (:obj:`Any`): A Python object

        Keyword Arguments:
            make_list_list (:obj:`bool`): Whether to make a list a list of a list


        Returns:
            :obj:`List`: The object wrapped in a list (or the original list)
        """

        if make_list_list and type(obj) is list and type(obj[0]) is not list:
            return [obj]
        elif type(obj) is list:
            return obj
        else:
            return [obj]

    @staticmethod
    def expand_list(
        l: List, length: int, with_value: Any = None, with_none: bool = False
    ) -> List:
        """ Expands list to a given length by repeating the last element.

        Arguments:
            l (:obj:`List`): A list
            length (:obj:`int`): The new length of the list
        
        Keyword Arguments:
            with_value (:obj:`Any`, optional): Whether to expand the list with a given value
            with_none (:obj:`bool`, optional): Whether to expand the list with None rather than the last element

        Returns:
            :obj:`List`: A list of length :obj:`length`
        """

        if with_none:
            l.extend([None] * (length - len(l)))
        elif with_value is not None:
            l.extend([with_value] * (length - len(l)))
        else:
            l.extend([l[-1]] * (length - len(l)))
        return l

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

    @staticmethod
    def in_notebook() -> bool:
        """Checks whether the code is running in an ipython notebook.

        Returns:
            :obj:`bool`: Whether the code is running in an ipython notebook
        """
        try:
            if (
                str(type(get_ipython()))
                == "<class 'ipykernel.zmqshell.ZMQInteractiveShell'>"
            ):
                return True
            else:
                return False
        except NameError:
            return False

    @staticmethod
    def create_categories(values: List[str]) -> Tuple[List[Tuple[int, str]], List[int]]:
        """ Creates a object which can be used as legend_labels and a list of
        the values as integers (after mapping strings to integers).

            Arguments:
                values (:obj:`List[str]`): A list of strings
            
            Returns:
                :obj:`Tuple[List[Tuple[int, str]], List[int]]`: A legend_labels object and a list of integers.
        """
        string_map = {}
        for i, value in enumerate(sorted(set(values))):
            string_map[value] = i

        legend_labels = []
        for key, value in string_map.items():
            legend_labels.append((value, key))

        return (legend_labels, [string_map[s] for s in values])
