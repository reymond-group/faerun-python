import random
import math
import numpy as np
import matplotlib.pyplot as plt
from yattag import Doc, indent


class Faerun(object):
    """ The faerun class
    """

    def __init__(self, title='python-faerun', point_size=5, tree_color='#aaaaaa', clear_color='#111111', fog_intensity=2.6, coords=True, coords_color='#888888', view='free', shader='circle'):
        self.title = title
        self.point_size = point_size
        self.tree_color = tree_color
        self.clear_color = clear_color
        self.fog_intensity = fog_intensity
        self.coords = coords
        self.coords_color = coords_color
        self.view = view
        self.shader = shader

        if view != 'free':
            self.fog_intensity = 0.0

    def plot(self, data, x='x', y='y', z='z', c='c', colormap='plasma', smiles='smiles', path='', tree=None):
        
        # print(self.create_html(tree))
        with open(path + 'index.html', 'w') as f:
            f.write(self.create_html(tree))
        with open(path + 'data.js', 'w') as f:
            f.write(self.create_data(data, { 'x': x, 'y': y, 'z': z, 'c': c, 'smiles': smiles }, colormap, tree))

    def get_css(self):
        return """
      body { margin: 0px; padding: 0px; height: 100%; user-select: none; overflow: hidden; }
      #lore { position: absolute; width: 100%; height: 100%; }
      #smiles-canvas { position: absolute; z-index: 9999; left: -999px; top: -999px; width: 250px; height: 250px; }
      #tip-image-container { position: absolute; z-index: 9999; width: 250px; height: 250px; background-color: rgba(255, 255, 255, 0.75); border-radius: 50%; pointer-events: none; opacity: 0.0; transition: opacity 0.1s ease-out; }
      #tip-image-container.show { opacity: 1.0; transition: opacity 0.1s ease-out; }
      #tip-image { pointer-events: none; filter: drop-shadow(0px 0px 5px rgba(255, 255, 255, 1.0)); }
      #selected { position: absolute; z-index: 9997; left: 5px; right: 5px; bottom: 25px; height: 100px; padding: 5px;
                  border: 2px solid rgba(255, 255, 255, 0.1); background-color: rgba(0, 0, 0, 0.9);
                  overflow-y: auto; overflow-x: hidden; color: #eeeeee;
                  font-family: Consolas, monaco, monospace; font-size: 0.8em;
                  user-select: text }
      #controls { position: absolute; z-index: 9998; left: 5px; right: 5px; bottom: 5px;
                  text-align: right; font-size: 0.7em;
                  font-family: Verdana, sans-serif; }
      #controls a { padding: 5px; color: #ccc; text-decoration: none; }
      #controls a:hover { color: #fff }
      #hover-indicator { display: none; position: absolute; z-index: 999; border: 1px solid #fff;
                         background-color: rgba(255, 255, 255, 0.25); border-radius: 50%; pointer-events: none; }
      #hover-indicator.show { display: block !important }
    """

    def get_js(self, tree):
        output = """
        let clearColor = '{}';
        let shader = '{}';
        let alphaBlending = false;
        let antialiasing = false;

        if (shader === 'circle') {{
            shader = 'smoothCircle';
            alphaBlending = true;
        }} else if (shader === 'legacyCircle') {{
            shader = 'circle';
            antialiasing = true;
        }}

        let smilesDrawer = new SmilesDrawer.Drawer({{ width: 250, height: 250 }});
        let lore = Lore.init('lore', {{ antialiasing: antialiasing, clearColor: clearColor, alphaBlending: alphaBlending }});
        let pointHelper = new Lore.Helpers.PointHelper(lore, 'python-lore', shader);
        let currentPoint = null;
        pointHelper.setXYZRGBS(data.x, data.y, data.z, data.r, data.g, data.b);
        pointHelper.setPointScale({:f});

        let cc = Lore.Core.Color.fromHex(clearColor);
        pointHelper.setFog([cc.components[0], cc.components[1], cc.components[2], cc.components[3]], {:f})

        lore.controls.setLookAt(pointHelper.getCenter());
        lore.controls.setRadius(pointHelper.getMaxRadius() + 100);
        lore.controls.setView(0.9, -0.5)

        let octreeHelper = new Lore.Helpers.OctreeHelper(lore, 'OctreeGeometry', 'tree', pointHelper);
        let tip = document.getElementById('tip-image-container');
        let tipImage = document.getElementById('tip-image');
        let canvas = document.getElementById('smiles-canvas');
        let hoverIndicator = document.getElementById('hover-indicator');

        octreeHelper.addEventListener('hoveredchanged', function(e) {{
            if (e.e) {{
                currentPoint = {{ index: e.e.index, smiles: data.smiles[e.e.index] }}
                SmilesDrawer.parse(data.smiles[e.e.index], function(tree) {{
                    smilesDrawer.draw(tree, 'smiles-canvas', 'light', false);
                    tipImage.src = canvas.toDataURL();
                    tip.classList.add('show');
                }});

                let pointSize = pointHelper.getPointSize();
                let x = octreeHelper.hovered.screenPosition[0];
                let y = octreeHelper.hovered.screenPosition[1];

                hoverIndicator.style.width = pointSize + 'px';
                hoverIndicator.style.height = pointSize + 'px';
                hoverIndicator.style.left = (x - pointSize / 2.0 - 1) + 'px';
                hoverIndicator.style.top = (y - pointSize / 2.0 - 1) + 'px';

                hoverIndicator.classList.add('show');
            }} else {{
                currentPoint = null;
                tip.classList.remove('show');
                hoverIndicator.classList.remove('show');
            }}
        }});
        """.format(self.clear_color, self.shader, self.point_size, self.fog_intensity)

        if self.view == 'front':
            output += "lore.controls.setFrontView();\n"
        elif self.view == 'back':
            output += "lore.controls.setBackView();\n"
        elif self.view == 'left':
            output += "lore.controls.setLeftView();\n"
        elif self.view == 'right':
            output += "lore.controls.setRightView();\n"
        elif self.view == 'bottom':
            output += "lore.controls.setBottomView();\n"
        elif self.view == 'top':
            output += "lore.controls.setTopView();\n"

        if self.coords:
            output += """
      let coord_options = {{
        axis: {{
          x: {{ color: Lore.Core.Color.fromHex('{}') }},
          y: {{ color: Lore.Core.Color.fromHex('{}') }},
          z: {{ color: Lore.Core.Color.fromHex('{}') }}
        }},
        ticks: {{
          x: {{ color: Lore.Core.Color.fromHex('{}') }},
          y: {{ color: Lore.Core.Color.fromHex('{}') }},
          z: {{ color: Lore.Core.Color.fromHex('{}') }}
        }},
        box: {{ enabled: false }}
      }}

        coordinateHelper = Lore.Helpers.CoordinatesHelper.fromPointHelper(
            pointHelper, coord_options)
      """.format(self.coords_color, self.coords_color, self.coords_color, self.coords_color, self.coords_color, self.coords_color)

        if tree:
            output += """
        let treeHelper = new Lore.Helpers.TreeHelper(lore, 'TreeGeometry', 'tree')
        treeHelper.setPositionsXYZHSS(
            data.edgeX, data.edgeY, data.edgeZ, Lore.Core.Color.hexToFloat('{}'), 1.0, 0.5)
      """.format(self.tree_color)

        output += """
      document.addEventListener('mousemove', function (event) {
        let tip = document.getElementById('tip-image-container');

        let x = event.clientX;
        let y = event.clientY - 48;

        if (x > window.innerWidth - 300) {
          x -= 250;
        }

        if (y > window.innerHeight - 300) {
          y -= 250;
        }

        if (tip) {
          tip.style.top = y + 'px';
          tip.style.left = x + 'px';
        }
      });
    """

        output += """
      let selected = document.getElementById('selected');
      document.addEventListener('dblclick', function (event) {
        if (currentPoint) {
          selected.innerHTML += currentPoint.smiles + '<br />';
          selected.scrollTop = selected.scrollHeight;
        }
      });
    """

        output += """
      let clear = document.getElementById('clear');
      clear.addEventListener('click', function(event) {
        event.preventDefault();
        selected.innerHTML = '';
      }, false);
    """

        # Register shortcuts
        output += """
      let hide = document.getElementById('hide');
      let toggleConsole = function () {
        selected.style.display = selected.style.display == 'none' ? 'block' : 'none';
        // controls.style.display = controls.style.display == 'none' ? 'block' : 'none';
      }

      let controls = document.getElementById('controls');
      document.addEventListener('keypress', function(event) {
        if (event.keyCode === 67 || event.keyCode === 99) {
          toggleConsole();
        }
      });
      hide.addEventListener('click', toggleConsole);
      hide.click();
    """

        return output

    def create_data(self, data, mapping, colormap, tree=None):
        output = 'const data = {\n'
        
        if mapping['z'] not in data:
            data[mapping['z']] = [0] * len(data[mapping['x']])

        # Normalize the data
        s = 750

        min_all = min([min(data[mapping['x']]), min(data[mapping['y']]), min(data[mapping['z']])])
        diff_all = max([max(data[mapping['x']]), max(data[mapping['y']]), max(data[mapping['z']])]) - min_all

        output += 'x: [' + ','.join(map(str, [round(s * (x - min_all) / diff_all, 3) for x in data[mapping['x']]])) + '],\n'
        output += 'y: [' + ','.join(map(str, [round(s * (y - min_all) / diff_all, 3) for y in data[mapping['y']]])) + '],\n'
        output += 'z: [' + ','.join(map(str, [round(s * (z - min_all) / diff_all, 3) for z in data[mapping['z']]])) + '],\n'
            
        
        if mapping['smiles'] in data:
            output += 'smiles: [' + ','.join('\'{0}\''.format(s) for s in data[mapping['smiles']]) + '],\n'
        
        if mapping['c'] in data:
            colors = np.array([plt.cm.get_cmap(colormap)(x) for x in data[mapping['c']]])
            colors = np.round(colors * 255.0)
            output += 'r: [' + ','.join(map(str, colors[:,0])) + '],\n'
            output += 'g: [' + ','.join(map(str, colors[:,1])) + '],\n'
            output += 'b: [' + ','.join(map(str, colors[:,2])) + '],\n'

        if tree is not None:
            x = []
            y = []
            z = []

            for pair in tree:
                x.append(data['x'][pair[0]])
                x.append(data['x'][pair[1]])
                y.append(data['y'][pair[0]])
                y.append(data['y'][pair[1]])
                z.append(data['z'][pair[0]])
                z.append(data['z'][pair[1]])

            output += 'edgeX: [' + ','.join(map(str, x)) + '],\n'
            output += 'edgeY: [' + ','.join(map(str, y)) + '],\n'
            output += 'edgeZ: [' + ','.join(map(str, z)) + '],\n'

        output += '};\n'

        return output

    def create_html(self, tree = None):
        # Create the HTML file
        doc, tag, text, line = Doc().ttl()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.asis('<meta charset="UTF-8">')
                line('title', self.title)
                line('script', '', src='https://unpkg.com/lore-engine@1.0.18/dist/lore.js')
                line('script', '', src='https://unpkg.com/smiles-drawer@1.0.2/dist/smiles-drawer.min.js')
                with tag('style'):
                    text(self.get_css())

            with tag('body'):
                line('canvas', '', id='smiles-canvas')
                line('div', '', id='hover-indicator')
                line('div', '', id='selected')
                with tag('div', '', id='controls'):
                    doc.asis('<a href="#" id="clear">&#8416;&nbsp;&nbsp;CLEAR</a>')
                    doc.asis('<a href="#" id="hide" title="Press c to toggle visibility of the console">_&nbsp;CONSOLE</a>')
                    doc.asis('<a href="https://github.com/reymond-group/faerun-python" id="clear">?&nbsp;HELP</a>')
                with tag('div', '', id='tip-image-container'):
                    doc.stag('img', id='tip-image')
                line('canvas', '', id='lore')
                line('script', '', src='data.js')
                with tag('script'):
                    doc.asis(self.get_js(tree is not None))

        return indent(doc.getvalue())
