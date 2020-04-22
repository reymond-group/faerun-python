import numpy as np
import pandas as pd
from faerun import Faerun
import pickle


faerun = Faerun(view="free", clear_color="#222222")

t = np.linspace(0, 12.0, 326)
s = np.sin(np.pi * t)
c = np.cos(np.pi * t)
sizes = np.linspace(0.1, 2.0, 326)

data = {"x": t, "y": s, "z": c, "c": t / max(t) * 100.0, "s": sizes}

data2 = {"x": t, "y": c, "z": s, "c": t / max(t), "s": sizes, "labels": sizes}

x = np.linspace(0, 12.0, 326)
c = np.random.randint(0, 6, len(x))
data3 = {
    "x": x,
    "y": np.random.rand(len(x)) - 0.5,
    "z": np.random.rand(len(x)) - 0.5,
    "c": [c, x],
    "cs": np.random.rand(len(x)),
    "s": [np.random.rand(len(x)), np.random.rand(len(x))],
    "labels": c,
}

legend_labels = [(0, "A"), (1, "B"), (2, "C"), (3, "D"), (4, "E"), (5, "F")]

df = pd.DataFrame.from_dict(data)
df2 = pd.DataFrame.from_dict(data2)

faerun.add_scatter(
    "sinus",
    df,
    shader="circle",
    point_scale=5.0,
    has_legend=True,
    legend_labels=[(0.0, "Low"), (50.0, "Inbetween"), (df["c"].max(), "High")],
)
faerun.add_scatter(
    "cosinus", df2, shader="sphere", point_scale=5.0, colormap="jet", has_legend=True
)
faerun.add_scatter(
    "categorical",
    data3,
    shader="sphere",
    point_scale=5.0,
    colormap=["Set1", "viridis"],
    has_legend=True,
    categorical=[True, False],
    legend_labels=legend_labels,
    series_title=["A", "B"],
    ondblclick=["console.log(labels[0])", "console.log('B:' + labels[0])"],
)

with open("index.pickle", "wb+") as handle:
    pickle.dump(faerun.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

file = open("index.pickle", "rb")
obj = pickle.load(file)
file.close()

faerun.plot(template="default")
