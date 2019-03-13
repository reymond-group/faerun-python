import numpy as np
import pandas as pd
from faerun import Faerun
import pickle


faerun = Faerun(view='free', clear_color='#222222')

t = np.linspace(0, 12.0, 326)
s = np.sin(np.pi * t)
c = np.cos(np.pi * t)
sizes = np.linspace(0.1, 2.0, 326)
 
data = {
    'x': t,
    'y': s,
    'z': c,
    'c': t / max(t),
    's': sizes
}

data2 = {
    'x': t,
    'y': c,
    'z': s,
    'c': t / max(t),
    's': sizes,
    'labels': sizes
}

df = pd.DataFrame.from_dict(data)
df2 = pd.DataFrame.from_dict(data2)

faerun.add_scatter('sinus', df, shader='circle', point_scale=5.0)
faerun.add_scatter('cosinus', df2, shader='sphere', point_scale=5.0)


with open('index.pickle', 'wb+') as handle:
    pickle.dump(faerun.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

file = open('index.pickle', 'rb')
obj = pickle.load(file)
file.close()
print(obj)

faerun.plot(template='default')
