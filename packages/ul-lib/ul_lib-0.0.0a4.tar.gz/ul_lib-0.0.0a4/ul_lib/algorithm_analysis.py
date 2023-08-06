import json
from pathlib import Path

from umap import UMAP
from sklearn.decomposition import PCA
import numpy as np
from matplotlib import pyplot as plt
from tqdm.auto import tqdm

from ul_lib.clustering import (
    Clustering,
    ClusteringWithOuters
)


class ClusteringResearcher:
    def __init__(self, model: Clustering, data, report_path: Path = None):
        self.model = model
        self.report_path = report_path
        self.data_space = {"raw": data}
        self.report = {}

    def scatter_map(
        self, values, title: str = None, out_space="umap", **kwargs
    ) -> Path:
        plt.figure(figsize=kwargs.get("figsize", (12, 10)))
        plt.scatter(
            self.data_space[out_space][:, 0],
            self.data_space[out_space][:, 1],
            c=values,
            edgecolor="none",
            alpha=kwargs.get("alpha", 0.4),
            s=40,
            cmap=plt.cm.get_cmap("nipy_spectral", len(np.unique(values))),
        )

        title = f"{title}"

        plt.title(title)
        if self.report_path and title:
            path = self.report_path / "plots" / f"{title}.jpg"
            plt.savefig(path)
            return path
        else:
            plt.show()

    def compute_umap(self, space="umap"):
        if space not in self.data_space:
            self.data_space[space] = UMAP().fit_transform(self.data_space["raw"])

    def compute_pca(self, n_components: int = 2, space="pca"):
        if space not in self.data_space:
            self.data_space[space] = PCA(n_components=n_components).fit_transform(
                self.data_space["raw"]
            )

    def compute_full_data_space(self):
        self.compute_umap()
        self.compute_pca()

    def analyze(
        self, space_in: str, space_out: str = "umap", title: str = None
    ) -> dict:
        values = self.model.clustering(self.data_space[space_in])
        report = {"metrics": self.model.metrics, "plots": {}}
        (self.report_path / "plots").mkdir(exist_ok=True)
        report["plots"]["result"] = self.scatter_map(
            values, f"{title} ({space_out})", space_out
        )
        if (
            isinstance(self.model, ClusteringWithOuters)
            and len(self.model.outers_indexes) > 0
        ):
            self.data_space["outers"] = np.array(
                [self.data_space[space_out][i] for i in self.model.outers_indexes]
            )
            report["plots"]["outers"] = self.scatter_map(
                [-1 for _ in self.data_space["outers"]],
                f"{title} ({space_out}) outers",
                "outers",
            )

            self.data_space["clean"] = np.array(
                [
                    self.data_space[space_out][i]
                    for i in range(len(self.data_space[space_out]))
                    if i not in self.model.outers_indexes
                ]
            )
            report["plots"]["clean"] = self.scatter_map(
                [v for v in self.model.result if v >= 0],
                f"{title} ({space_out}) clean",
                "clean",
            )
        return report

    def report_to_json(self):
        with open(self.report_path / "report.json", "w") as f:
            json.dump(self.report, f)

    def research(self, mode="raw", space_out: str = "umap"):
        if mode in self.data_space:
            self.report[f"{mode} space"] = self.analyze(mode, space_out, f"{mode} space")
        elif mode == "umap":
            self.compute_umap()
            self.report["umap space"] = self.analyze("umap", space_out, "umap space")
        elif mode == "pca":
            self.compute_pca()
            self.report["pca space"] = self.analyze("pca", space_out, "pca space")

        elif mode == "space_search":
            self.compute_full_data_space()
            spaces = self.data_space.keys()
            for space in tqdm(spaces):
                title = f"{space} space"
                self.report[title] = self.analyze(space, space_out, title)

        elif mode == "full":
            self.research(mode="space_search", space_out=space_out)
