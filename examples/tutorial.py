import pickle
import numpy as np
from faerun import Faerun


def main():
    f = Faerun(
        clear_color="#222222",
        coords=True,
        view="front",
    )

    x = np.linspace(0, 12.0, 326)
    y = np.sin(np.pi * x)
    z = np.cos(np.pi * x)
    c = np.random.randint(0, 2, len(x))

    data = {"x": x, "y": y, "z": z, "c": c, "labels": c}

    f.add_scatter(
        "helix",
        data,
        shader="smoothCircle",
        colormap="Dark2",
        point_scale=5.0,
        categorical=True,
        has_legend=True,
        legend_labels=[(0, "Zero"), (1, "One")],
    )

    f.plot("helix")

    with open("helix.faerun", "wb+") as handle:
        pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
