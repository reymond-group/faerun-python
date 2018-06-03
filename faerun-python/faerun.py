import numpy as np
from yattag import Doc, indent

class Faerun(object):
  """ The faerun class
  """
  def __init__(self, title='python-faerun', point_size=10, clear_color='#222222'):
    self.title = title
    self.point_size = point_size
    self.clear_color = clear_color
  
  def plot(self, path, data):
    print(faerun.create_html(data))
    with open(path, 'w') as f:
      f.write(faerun.create_html(data))
  
  def get_css(self):
    return """
      body { margin: 0px; padding: 0px; height: 100%; user-select: none; }
      #lore { position: absolute; width: 100%; height: 100%; }
      #smiles-canvas { position: absolute; z-index: 9999; left: -999px; top: -999px; width: 250px; height: 250px; }
      #tip-image-container { position: absolute; z-index: 9999; width: 250px; height: 250px; background-color: rgba(255, 255, 255, 0.75); border-radius: 50%; pointer-events: none; opacity: 0.0; transition: opacity 0.1s ease-out; }
      #tip-image-container.show { opacity: 1.0; transition: opacity 0.1s ease-out; }
      #tip-image { pointer-events: none; filter: drop-shadow(0px 0px 5px rgba(255, 255, 255, 1.0)); }
    """
  
  def get_js(self):
    return """
      let smilesDrawer = new SmilesDrawer.Drawer({{ width: 250, height: 250 }});
      let lore = Lore.init('lore', {{ clearColor: '{}' }});
      let pointHelper = new Lore.Helpers.PointHelper(lore, 'python-lore', 'sphere');
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
          SmilesDrawer.parse(smiles[e.e.index], function(tree) {{
            smilesDrawer.draw(tree, 'smiles-canvas', 'light', false);
            tipImage.src = canvas.toDataURL();
            tip.classList.add('show');
          }});
        }} else {{
          tip.classList.remove('show');
        }}
      }});
    """.format(self.clear_color, self.point_size)

  def get_data(self, data):
    output = ''

    for key, value in data.items():
      if key == 'smiles':
        output += 'let ' + key + ' = [' + str(value)[1:-1] + '];'
      else:
        output += 'let ' + key + ' = [' + ','.join(map(str,value)) + '];'

    return output

  def create_html(self, data):
    # Create the HTML file
    doc, tag, text, line = Doc().ttl()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      with tag('head'):
        doc.asis('<meta charset="UTF-8">')
        line('title', self.title)
        line('script', '', src='https://unpkg.com/lore-engine@1.0.7/dist/lore.js')
        line('script', '', src='https://unpkg.com/smiles-drawer@1.0.2/dist/smiles-drawer.min.js')
        with tag('style'):
          text(self.get_css())

      with tag('body'):
        line('canvas', '', id='smiles-canvas')
        with tag('div', '', id='tip-image-container'):
          doc.stag('img', id='tip-image')
        line('canvas', '', id='lore')
        with tag('script'):
          text(self.get_data(data))
        with tag('script'):
          text(self.get_js())

    return indent(doc.getvalue())


data = {
  'x': [10, 50, 100],
  'y': [20, 10, 60],
  'z': [50, 20, 80],
  'c': [0.1, 0.5, 0.7],
  'smiles': ['C1CCCC1', 'CNCNC(=O)C', 'CCCCCC']
}
  
faerun = Faerun()
faerun.plot('index.html', data)
