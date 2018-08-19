import random
import numpy as np
from yattag import Doc, indent

class Faerun(object):
  """ The faerun class
  """
  def __init__(self, title='python-faerun', point_size=10, tree_hue={ 'r': 132, 'g': 184, 'b': 217 }, clear_color='#222222', fog_intensity=6.0):
    self.title = title
    self.point_size = point_size
    self.tree_hue = tree_hue
    self.clear_color = clear_color
    self.fog_intensity = fog_intensity
  
  def plot(self, path, data, tree = None):
    print(self.create_html(tree))
    with open(path + 'index.html', 'w') as f:
      f.write(self.create_html(tree))
    with open(path + 'data.js', 'w') as f:
      f.write(self.create_data(data, tree))
  
  def get_css(self):
    return """
      body { margin: 0px; padding: 0px; height: 100%; user-select: none; }
      #lore { position: absolute; width: 100%; height: 100%; }
      #smiles-canvas { position: absolute; z-index: 9999; left: -999px; top: -999px; width: 250px; height: 250px; }
      #tip-image-container { position: absolute; z-index: 9999; width: 250px; height: 250px; background-color: rgba(255, 255, 255, 0.75); border-radius: 50%; pointer-events: none; opacity: 0.0; transition: opacity 0.1s ease-out; }
      #tip-image-container.show { opacity: 1.0; transition: opacity 0.1s ease-out; }
      #tip-image { pointer-events: none; filter: drop-shadow(0px 0px 5px rgba(255, 255, 255, 1.0)); }
      #selected { position: absolute; z-index: 9997; left: 5px; right: 5px; bottom: 5px; height: 100px; padding: 5px;
                  border: 2px solid rgba(255, 255, 255, 0.1); background-color: rgba(0, 0, 0, 0.9); 
                  overflow-y: auto; overflow-x: hidden; color: #eeeeee;
                  font-family: Consolas, monaco, monospace; font-size: 0.8em;
                  user-select: text }
      #controls { position: absolute; z-index: 9998; left: 5px; right: 5px; bottom: 120px;
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
      let smilesDrawer = new SmilesDrawer.Drawer({{ width: 250, height: 250 }});
      let lore = Lore.init('lore', {{ clearColor: clearColor }});
      let pointHelper = new Lore.Helpers.PointHelper(lore, 'python-lore', 'sphere');
      let currentPoint = null;
      pointHelper.setXYZHS(data.x, data.y, data.z, data.c, 1.0);
      pointHelper.setPointScale({:f});

      let cc = Lore.Core.Color.fromHex(clearColor);
      pointHelper.setFog([cc.components[0], cc.components[1], cc.components[2], cc.components[3]], {:f})

      lore.controls.setLookAt(pointHelper.getCenter());
      lore.controls.setRadius(pointHelper.getMaxRadius());

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
          hoverIndicator.style.left = (x - pointSize / 2.0 - 2) + 'px';
          hoverIndicator.style.top = (y - pointSize / 2.0 - 2) + 'px';

          hoverIndicator.classList.add('show');
        }} else {{
          currentPoint = null;
          tip.classList.remove('show');
          hoverIndicator.classList.remove('show');
        }}
      }});
    """.format(self.clear_color, self.point_size, self.fog_intensity)

    if tree:
      output += """
        let treeHelper = new Lore.Helpers.TreeHelper(lore, 'TreeGeometry', 'tree')
        treeHelper.setPositionsXYZHSS(data.edgeX, data.edgeY, data.edgeZ, Lore.Core.Color.rgbToFloat({:f}, {:f}, {:f}), 1.0, 0.5)
      """.format(self.tree_hue['r'], self.tree_hue['g'], self.tree_hue['b'])

    
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
        controls.style.display = controls.style.display == 'none' ? 'block' : 'none';
      }

      let controls = document.getElementById('controls');
      document.addEventListener('keypress', function(event) {
        if (event.keyCode === 67 || event.keyCode === 99) {
          toggleConsole();
        }
      });
      hide.addEventListener('click', toggleConsole);

    """

    return output

  def create_data(self, data, tree = None):
    output = 'const data = {\n'

    for key, value in data.items():
      if key == 'smiles':
        output += key + ': [' + str(value)[1:-1] + '],\n'
      else:
        output += key + ': [' + ','.join(map(str, value)) + '],\n'

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
        line('script', '', src='https://unpkg.com/lore-engine@1.0.17/dist/lore.js')
        line('script', '', src='https://unpkg.com/smiles-drawer@1.0.2/dist/smiles-drawer.min.js')
        with tag('style'):
          text(self.get_css())

      with tag('body'):
        line('canvas', '', id='smiles-canvas')
        line('div', '', id='hover-indicator')
        line('div', '', id='selected')
        with tag('div', '', id='controls'):
          doc.asis('<a href="#" id="clear">&#8416;&nbsp;&nbsp;CLEAR</a>')
          doc.asis('<a href="#" id="hide" title="Press c to toggle visibility of the console">&times;&nbsp;HIDE</a>')
          doc.asis('<a href="https://github.com/reymond-group/faerun-python" id="clear">?&nbsp;HELP</a>')
        with tag('div', '', id='tip-image-container'):
          doc.stag('img', id='tip-image')
        line('canvas', '', id='lore')
        line('script', '', src='data.js')
        with tag('script'):
          doc.asis(self.get_js(tree is not None))

    return indent(doc.getvalue())
  
faerun = Faerun()

# data = {
#   'x': [10, 50, 100],
#   'y': [20, 10, 60],
#   'z': [50, 20, 80],
#   'c': [0.1, 0.5, 0.7],
#   'smiles': ['C1CCCC1', 'CNCNC(=O)C', 'CCCCCC']
# }
# faerun.plot('', data, [(0, 1), (0, 2)])


x = []
y = []
z = []
c = []
smiles = []

for i in range(1000000):
  x.append(random.random() * 500)
  y.append(random.random() * 500)
  z.append(random.random() * 500)
  c.append(random.random())
  smiles.append('C1CCCCC1CC(=O)C')

data = {
  'x': x,
  'y': y,
  'z': z,
  'c': c,
  'smiles': smiles
}

faerun.plot('', data)
