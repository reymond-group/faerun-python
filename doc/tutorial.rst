Getting Started
---------------

Installation
^^^^^^^^^^^^
Faerun can be installed using pip.

.. code-block:: bash

   pip install faerun

In order to use it in a script, the class ``Faerun`` has to be imported from the package.

.. code-block:: python

   from faerun import Faerun

That's it for the installation.

Create a Plot Document
^^^^^^^^^^^^^^^^^^^^^^
In order to plot, a plot document has to be created. To do so, create an instance of the class ``Faerun``

.. code-block:: python

   from faerun import Faerun

   f = Faerun(title='faerun-example', clear_color='#222222', coords=False, view='free')

Here, we set the ``title`` of the plot document. This will be used as the title of the HTML document. The clear color of the canvas, which is the background color of the plot, is set to ``'#222222'`` (which is the hex-code for a dark gray).
The drawing of coordinate axes is disabled by setting ``coords=False`` and since we want to draw 3D data, the argument ``view`` is set to ``'free'`` to enable the user to pan and rotate the plot.

Preparing Data for Plotting
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The next step is to prepare the data which is to be plotted. In the tutorial, we will just generate some nice looking data using ``numpy``.

.. code-block:: python

    import numpy as np

    x = np.linspace(0, 12.0, 326)
    y = np.sin(np.pi * x)
    z = np.cos(np.pi * x)
    c = np.random.randint(0, 6, len(x))

This data can then be wrapped in a ``dict``. In addition, ``DataFrame`` from the ``pandas`` package are also supported by faerun. 
In the example, the same values are used for the colors ``c`` and labels ``labels``.

.. code-block:: python

    data = {'x': x, 'y': y, 'z': z, 'c': c, 'labels': c}

Adding a Scatter Layer
^^^^^^^^^^^^^^^^^^^^^^
Given the ``Faerun`` instance and the data, a scatter plot can be created using the method ``add_scatter``.

.. code-block:: python

    f.add_scatter('helix', data, shader='sphere', colormap='Dark2', point_scale=5.0, 
                  categorical=True, has_legend=True, legend_labels=[(0, 'Zero'), (1, 'One')])

The data is added as a scatter layer named helix. The chose shader will render the data points as 
spheres (with diffuse and specular lighting) of size 5.0 with colors from the ``matplotlib`` colormap ``'Dark2'``. 
As the ``c`` is categorical, the parameter ``categorical`` is set to ``True``, otherwise ``matplotlib`` will mess up the values.

Finally, ``has_legend=True`` adds the scatter layer to the legend and ``legend_labels`` is a ``list`` of ``tuple``, associating values with a label.

Saving to HTML
^^^^^^^^^^^^^^
The faerun document can the be plotted to an HTML document with an accompanying JavaScript data file.

.. code-block:: python

    f.plot('helix')

This saves the plot as ``helix.html` and ``helix.js``. The files can be opened locally or hosted on any web server.

.. image:: _static/tutorial.png
   :alt: A helix drawn using faerun.

Saving to Faerun Data File
^^^^^^^^^^^^^^^^^^^^^^^^^^
The faerun document can also be exported to a faerun data file, which in turn can then be hosted using the ``web`` module.

.. code-block:: python

    import pickle

    with open('helix.faerun', 'wb+') as handle:
        pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

Complete Example
^^^^^^^^^^^^^^^^
.. code-block:: python

    import pickle
    import numpy as np
    from faerun import Faerun

    def main():
        f = Faerun(title='faerun-example', clear_color='#222222', coords=False, view='free')

        x = np.linspace(0, 12.0, 326)
        y = np.sin(np.pi * x)
        z = np.cos(np.pi * x)
        c = np.random.randint(0, 2, len(x))

        data = {'x': x, 'y': y, 'z': z, 'c': c, 'labels': c}

        f.add_scatter('helix', data, shader='sphere', colormap='Dark2', point_scale=5.0, 
                    categorical=True, has_legend=True, legend_labels=[(0, 'Zero'), (1, 'One')])

        f.plot('helix')

        with open('helix.faerun', 'wb+') as handle:
            pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    if __name__ == '__main__':
        main()

