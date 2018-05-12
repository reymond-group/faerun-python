import numpy as np
from yattag import Doc, indent

class Faerun(object):
  """ The faerun class
  """
  def __init__(self, dimensions, title='python-faerun'):
    self.dimensions = dimensions
    self.title = title
  
  def write(self, path, data):
    with open(path) as f:
      f.write('')
  
  def get_css(self):
    return """
      body { margin: 0px; padding: 0px; height: 100%; user-select: none; }
      #lore { position: absolute; width: 100%; height: 100%; }
      #tip-image-container { position: absolute; z-index: 9999; width: 250px; height: 250px; background-color: rgba(255, 255, 255, 0.75); border-radius: 50%; pointer-events: none; opacity: 0.0; transition: opacity 0.1s ease-out; }
      #tip-image-container.show { opacity: 1.0; transition: opacity 0.1s ease-out; }
      #tip-image { pointer-events: none; filter: drop-shadow(0px 0px 5px rgba(255, 255, 255, 1.0)); }
    """
  
  def get_js(self):
    return """
      let smilesDrawer = new SmilesDrawer.Drawer({ width: 250, height: 250 });
      let lore = Lore.init('lore', { clearColor: '#222222' });
    """

  def create_html(self):
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
        with tag('div', '', id='tip-image-container'):
          doc.stag('img', id='tip-image')
        line('canvas', '', id='lore')
        with tag('script'):
          text(self.get_js())

    return indent(doc.getvalue())

  
faerun = Faerun(2)
print(faerun.create_html())
with open('index.html', 'w') as f:
  f.write(faerun.create_html())