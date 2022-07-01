from cProfile import label
from typing import Union, List, Iterable, Optional
from tmap.core import TMAPEmbedding
from faerun import Faerun
from matplotlib.colors import Colormap


class FaerunPlot:
    def __init__(
        self,
        clear_color: str = "#222222",
        coords: bool = False,
        view: str = "front",
        thumbnail_fixed: bool = False,
        impress: Optional[str] = None,
    ):
        if impress is None:
            impress = 'made with <a href="http://tmap.gdb.tools" target="_blank">tmap</a><br />and <a href="https://github.com/reymond-group/faerun-python" target="_blank">faerun</a><br /><a href="https://gist.github.com/daenuprobst/5cddd0159c0cf4758fb16b4b4acbef89">source</a>'

        self.f = Faerun(
            clear_color=clear_color,
            coords=coords,
            view=view,
            impress=impress,
            thumbnail_fixed=thumbnail_fixed,
        )

    def add_series(
        self,
        x: Iterable,
        y: Iterable,
        c: Union[List, List[List]],
        z: Optional[Iterable] = None,
        labels: Optional[List] = None,
        cmap: Union[Union[str, Colormap], List[Union[str, Colormap]]] = "viridis",
        categorical: Union[bool, List[bool]] = False,
        shader: str = "smoothCircle",
        point_scale: float = 2.0,
        title: Optional[Union[str, List[str]]] = None,
        show_legend: bool = True,
        legend_title: str = "",
        name: Optional[str] = None,
    ) -> str:
        multiple_c = any(isinstance(el, list) for el in c)
        n_c = 1

        if multiple_c:
            n_c = len(c)

        if title is None:
            if multiple_c:
                title = [str(i + 1) for i in range(n_c)]
            else:
                title = "1"

        if name is None:
            name = "Series" + str(len(self.f.scatters) + 1)

        data = {
            "x": x,
            "y": y,
            "c": c,
        }

        if z is not None:
            data["z"] = z

        if labels is not None:
            data["labels"] = labels

        self.f.add_scatter(
            name,
            data,
            shader=shader,
            colormap=cmap,
            point_scale=point_scale,
            categorical=categorical,
            has_legend=show_legend,
            # legend_labels=[],
            # selected_labels=["SMILES", "Drugbank ID", "Name"],
            series_title=title,
            # max_legend_label=[
            #     None,
            #     None,
            #     None,
            #     None,
            #     None,
            #     str(round(max(tpsa))),
            #     str(round(max(logp))),
            #     str(round(max(mw))),
            #     str(round(max(h_acceptors))),
            #     str(round(max(h_donors))),
            #     str(round(max(ring_count))),
            # ],
            # min_legend_label=[
            #     None,
            #     None,
            #     None,
            #     None,
            #     None,
            #     str(round(min(tpsa))),
            #     str(round(min(logp))),
            #     str(round(min(mw))),
            #     str(round(min(h_acceptors))),
            #     str(round(min(h_donors))),
            #     str(round(min(ring_count))),
            # ],
            # title_index=2,
            legend_title=legend_title,
        )

        return name

    def add_tree(self, target: str, s: Iterable, t: Iterable, color: str = "#666666"):
        self.f.add_tree(
            target + "Tree", {"from": s, "to": t}, point_helper=target, color=color
        )

    def add_tmap_series(
        self,
        tmap_embedding: TMAPEmbedding,
        c: Union[List, List[List]],
        z: Optional[Iterable] = None,
        labels: Optional[List] = None,
        cmap: Union[str, Colormap] = "viridis",
        categorical: bool = False,
        shader: str = "smoothCircle",
        point_scale: float = 2.0,
        title: str = None,
        show_legend: bool = True,
        legend_title: str = "",
        name: Optional[str] = None,
        add_tree: bool = True,
        tree_color: str = "#888888",
    ):

        series_name = self.add_series(
            tmap_embedding.x,
            tmap_embedding.y,
            c=c,
            z=z,
            labels=labels,
            cmap=cmap,
            categorical=categorical,
            shader=shader,
            point_scale=point_scale,
            title=title,
            show_legend=show_legend,
            legend_title=legend_title,
            name=name,
        )

        if add_tree:
            self.add_tree(series_name, tmap_embedding.s, tmap_embedding.t, tree_color)

    def save(self, name, template="default"):
        self.f.plot(name, template=template)
