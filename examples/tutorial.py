import pickle
import numpy as np
from faerun import Faerun


def main():
    f = Faerun(clear_color="#222222", coords=True, view="front")

    x = np.linspace(0, 12.0, 326)
    y = np.sin(np.pi * x)
    z = np.cos(np.pi * x)
    c = np.random.randint(0, 2, len(x))

    labels = [str(l) + "__Test" for l in c]

    data = {"x": x, "y": y, "z": z, "c": c, "labels": labels}

    f.add_scatter(
        "helix",
        data,
        shader="smoothCircle",
        colormap="Dark2",
        point_scale=5.0,
        categorical=True,
        has_legend=True,
        legend_labels=[(0, "Zero"), (1, "One")],
        selected_labels=["None", "Just a Small Test"],
    )

    f.add_tree(
        "helixtree", {"from": [1, 5, 6, 7], "to": [2, 7, 8, 9]}, point_helper="helix"
    )

    f.plot("helix")

    with open("helix.faerun", "wb+") as handle:
        pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
