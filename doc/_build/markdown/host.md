# Web

## Introduction

While small plots can easily be created and stored in a single HTML and JavaScript file, which are then loaded completely in the browsers memory, this is not possible for larger data sets due to browser limitations.
In order to solve this problem, Faerun includes a small HTTP server (based on cherrypy) to serve the data to the browser.

## Creating Faerun Data Files

As shown in Getting Started, Faerun can save data as `.faerun` data files using `pickle`.

```
with open('helix.faerun', 'wb+') as handle:
    pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)
```

## Starting a Faerun Web Server

```
from faerun import host

host('helix.faerun', label_type='default',
     theme='dark')
```

## Formatting Labels

Labels can be formatted by defining a custom `label_formatter`. If no `label_formatter` is provided to the `host` function, the default is used:

```
label_formatter = lambda label, index, name: label.split('__')[0]
```

This default splits the label value on `'__'` to store different labels and enable search on different values the the displayed labels. See “Searching” for details. Defining a custom label formatter is straight forward. As an example, let’s prefix each label with a string and add their index and layer name:

```
def custom_label_formatter(label, index, name):
    return f'Example: {label} ({index}, {name})'

host('helix.faerun', label_type='default',
     theme='dark', label_formatter=custom_label_formatter)
```

This function is then called whenever a label is requested from the server. In addition to the argument `label`, the arguments `index` and `name` can be used to further customize the displayed label and represent the integer index of the data point and the data layer they belong to (e.g. the name defined with `add_scatter`).



![image](_static/tutorial_host_label.png)

## Adding Hyperlinks

Faerun allows to link the data to an arbitrary URL which can be visited upon double-clicking a data point. In order to do this, a `link_formatter` has to be provided. This works similar to customizing the label.

```
def custom_link_formatter(label, index, name):
    return f'https://www.google.com/search?q={label}'

host('helix.faerun', label_type='default',
     theme='dark', link_formatter=custom_link_formatter)
```

## Searching

The hosted version of a Faerun visualization also allows for searching. As a default, the search searches for exact matches in labels (substring or regex searches are not possible at this time).



![image](_static/tutorial_host_search.png)

However, the search can be customized. As described in “Formatting Labels”, additional label values can be added by separating them using `'__'`.

```
c = np.random.randint(0, 2, len(x))
labels = [''] * len(c)

for i, e in enumerate(c):
    labels[i] = str(e) + '__' + str(i % 20)

data = {'x': x, 'y': y, 'z': z, 'c': c, 'labels': labels}
```

The above examples adds an additional label value and as default, the second label value is then used by the search.



![image](_static/tutorial_host_search_2.png)

If there are additional label values, the search index can be set using the `search_index` argument.

## Add Info / Documentation

As the visualization is ready to be deployed to a publicly accessible web server, it might be of interest to add a documentation. The `host` method supports the argument `info` that accepts a (markdown formatted) string. This information is the desplayed on the generated web page.

```
info = ('#Welcome to Fearun',
        'This is a small Faerun example.'
        '',
        'Yay markdown! This means that you can easily:',
        '- Add lists',
        '- Build tables',
        '- Insert images and links',
        '- Add code examples',
        '- ...'
       )

host('helix.faerun', label_type='default', theme='dark',
    label_formatter=custom_label_formatter, link_formatter=custom_link_formatter,
    info='\n'.join(info))
```

An info button is then shown next to the screenshot button, which upon click opens a window containing the info.

## Complete Example

```
import pickle
import numpy as np
from faerun import Faerun, host


def main():
    f = Faerun(title='faerun-example', clear_color='#222222', coords=False, view='free')

    x = np.linspace(0, 12.0, 326)
    y = np.sin(np.pi * x)
    z = np.cos(np.pi * x)
    c = np.random.randint(0, 2, len(x))

    labels = [''] * len(c)

    for i, e in enumerate(c):
        labels[i] = str(e) + '__' + str(i % 20)

    data = {'x': x, 'y': y, 'z': z, 'c': c, 'labels': labels}

    f.add_scatter('helix', data, shader='sphere', colormap='Dark2', point_scale=5.0,
                categorical=True, has_legend=True, legend_labels=[(0, 'Zero'), (1, 'One')])

    f.plot('helix')

    with open('helix.faerun', 'wb+') as handle:
        pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    def custom_label_formatter(label, index, name):
        return f'Example: {label} ({index}, {name})'

    def custom_link_formatter(label, index, name):
        return f'https://www.google.com/search?q={label}'

    info = ('#Welcome to Fearun',
            'This is a small Faerun example.'
            '',
            'Yay markdown! This means that you can easily:',
            '- Add lists',
            '- Build tables',
            '- Insert images and links',
            '- Add code examples',
            '- ...'
        )

    host('helix.faerun', label_type='default', theme='dark',
        label_formatter=custom_label_formatter, link_formatter=custom_link_formatter,
        info='\n'.join(info))


if __name__ == '__main__':
    main()
```
