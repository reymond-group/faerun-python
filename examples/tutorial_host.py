import pickle
import numpy as np
from faerun import Faerun, host


def main():
    f = Faerun(title="faerun-example", clear_color="#222222", coords=False, view="free")

    x = np.linspace(0, 12.0, 326)
    y = np.sin(np.pi * x)
    z = np.cos(np.pi * x)
    c = np.random.randint(0, 2, len(x))

    labels = [""] * len(c)

    for i, e in enumerate(c):
        labels[i] = str(e) + "__" + str(i % 20)

    data = {"x": x, "y": y, "z": z, "c": c, "labels": labels}

    f.add_scatter(
        "helix",
        data,
        shader="sphere",
        colormap="Dark2",
        point_scale=5.0,
        categorical=True,
        has_legend=True,
        legend_labels=[(0, "Zero"), (1, "One")],
    )

    f.plot("helix")

    with open("helix.faerun", "wb+") as handle:
        pickle.dump(f.create_python_data(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    def custom_label_formatter(label, index, name):
        return f"Example: {label} ({index}, {name})"

    def custom_link_formatter(label, index, name):
        return f"https://www.google.com/search?q={label}"

    info = (
        "#Welcome to Fearun",
        "This is a small Faerun example." "",
        "Yay markdown! This means that you can easily:",
        "- Add lists",
        "- Build tables",
        "- Insert images and links",
        "- Add code examples",
        "- ...",
    )

    host(
        "helix.faerun",
        label_type="default",
        title="Helix",
        theme="dark",
        label_formatter=custom_label_formatter,
        link_formatter=custom_link_formatter,
        info="\n".join(info),
    )


if __name__ == "__main__":
    main()
