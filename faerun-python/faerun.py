import numpy as np
from yattag import Doc, indent

class Faerun(object):
  """ The faerun class
  """
  def __init__(self, title='python-faerun', point_size=10, tree_hue=0.5, clear_color='#222222'):
    self.title = title
    self.point_size = point_size
    self.tree_hue = tree_hue
    self.clear_color = clear_color
  
  def plot(self, path, data, tree = None):
    print(self.create_html(data, tree))
    with open(path, 'w') as f:
      f.write(self.create_html(data, tree))
  
  def get_css(self):
    return """
      body { margin: 0px; padding: 0px; height: 100%; user-select: none; }
      #lore { position: absolute; width: 100%; height: 100%; }
      #smiles-canvas { position: absolute; z-index: 9999; left: -999px; top: -999px; width: 250px; height: 250px; }
      #tip-image-container { position: absolute; z-index: 9999; width: 250px; height: 250px; background-color: rgba(255, 255, 255, 0.75); border-radius: 50%; pointer-events: none; opacity: 0.0; transition: opacity 0.1s ease-out; }
      #tip-image-container.show { opacity: 1.0; transition: opacity 0.1s ease-out; }
      #tip-image { pointer-events: none; filter: drop-shadow(0px 0px 5px rgba(255, 255, 255, 1.0)); }
      #selected { position: absolute; z-index: 9998; left: 5px; right: 5px; bottom: 5px; height: 100px; padding: 5px;
                  border: 2px solid rgba(255, 255, 255, 0.1); background-color: rgba(0, 0, 0, 0.9); 
                  overflow-y: auto; overflow-x: hidden; color: #eeeeee;
                  font-family: Consolas, monaco, monospace; font-size: 0.8em;
                  user-select: text }
    """
  
  def get_js(self, tree):
    output = """
      let smilesDrawer = new SmilesDrawer.Drawer({{ width: 250, height: 250 }});
      let lore = Lore.init('lore', {{ clearColor: '{}' }});
      let pointHelper = new Lore.Helpers.PointHelper(lore, 'python-lore', 'sphere');
      let currentPoint = null;
      pointHelper.setPositionsXYZHSS(x, y, z, c, 1.0, 1.0);
      pointHelper.setPointScale({:f});
      lore.controls.setLookAt(pointHelper.getCenter());
      lore.controls.setRadius(pointHelper.getMaxRadius());

      let octreeHelper = new Lore.Helpers.OctreeHelper(lore, 'OctreeGeometry', 'tree', pointHelper);
      let tip = document.getElementById('tip-image-container');
      let tipImage = document.getElementById('tip-image');
      let canvas = document.getElementById('smiles-canvas');

      octreeHelper.addEventListener('hoveredchanged', function(e) {{
        if (e.e) {{
          currentPoint = {{ index: e.e.index, smiles: smiles[e.e.index] }}
          SmilesDrawer.parse(smiles[e.e.index], function(tree) {{
            smilesDrawer.draw(tree, 'smiles-canvas', 'light', false);
            tipImage.src = canvas.toDataURL();
            tip.classList.add('show');
          }});
        }} else {{
          currentPoint = null;
          tip.classList.remove('show');
        }}
      }});
    """.format(self.clear_color, self.point_size)

    if tree:
      output += """
        let treeHelper = new Lore.Helpers.TreeHelper(lore, 'TreeGeometry', 'tree')
        treeHelper.setPositionsXYZHSS(edgeX, edgeY, edgeZ, {:f}, 1.0, 0.5)
      """.format(self.tree_hue)

    
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
        }
      });
    """

    output += """
      let download = document.getElementById('download');

      download.addEventListener('click', function(event) {
        download.href = document.getElementById('lore').toDataURL();
        download.download = "faerun-snapshot.png";
      }, false);
    """

    return output

  def get_data(self, data, tree):
    output = ''

    for key, value in data.items():
      if key == 'smiles':
        output += 'let ' + key + ' = [' + str(value)[1:-1] + '];\n'
      else:
        output += 'let ' + key + ' = [' + ','.join(map(str, value)) + '];\n'

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

      output += 'let edgeX = [' + ','.join(map(str, x)) + '];\n'
      output += 'let edgeY = [' + ','.join(map(str, y)) + '];\n'
      output += 'let edgeZ = [' + ','.join(map(str, z)) + '];\n'

    return output

  def create_html(self, data, tree = None):
    # Create the HTML file
    doc, tag, text, line = Doc().ttl()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      with tag('head'):
        doc.asis('<meta charset="UTF-8">')
        line('title', self.title)
        line('script', '', src='https://unpkg.com/lore-engine@1.0.9/dist/lore.js')
        line('script', '', src='https://unpkg.com/smiles-drawer@1.0.2/dist/smiles-drawer.min.js')
        with tag('style'):
          text(self.get_css())

      with tag('body'):
        line('canvas', '', id='smiles-canvas')
        line('div', '', id='selected')
        with tag('div', '', id='controls'):
          line('a', 'Save Snapshot', id='download', href='#')
        with tag('div', '', id='tip-image-container'):
          doc.stag('img', id='tip-image')
        line('canvas', '', id='lore')
        with tag('script'):
          doc.asis(self.get_data(data, tree))
        with tag('script'):
          doc.asis(self.get_js(tree is not None))

    return indent(doc.getvalue())

data = {
  'x': [10, 50, 100],
  'y': [20, 10, 60],
  'z': [50, 20, 80],
  'c': [0.1, 0.5, 0.7],
  'smiles': ['C1CCCC1', 'CNCNC(=O)C', 'CCCCCC']
}
  
faerun = Faerun()
faerun.plot('index.html', data, [(0, 1), (0, 2)])
