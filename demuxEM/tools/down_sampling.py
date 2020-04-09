import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

from pegasusio import read_input, UnimodalData
from . import estimate_background_probs, demultiplex


def down_sampling(rna_gt: UnimodalData, hto_gt: UnimodalData, probs: List[float], n_threads: int = 1):
    f = np.vectorize(lambda x, p: np.random.binomial(int(x + 1e-4), p, size=1)[0])

    nsample = rna_gt.shape[0]
    nhto = hto_gt.X.sum()

    fracs = []
    accuracy = []
    for p in probs:
        rna_data = rna_gt.copy()
        hto_data = hto_gt.copy()

        hto_data.X.data = f(hto_data.X.data, p)
        idx = hto_data.X.sum(axis=1).A1 > 0
        hto_data = hto_data[idx,].copy(deep = False)
        fracs.append(hto_data.X.sum() / nhto)

        estimate_background_probs(hto_data)
        demultiplex(rna_data, hto_data, n_threads=n_threads)
        accuracy.append(
            sum(
                rna_data.obs["assignment"].values.astype("str")
                == rna_gt.obs["assignment"].values.astype("str")
            )
            / nsample
        )

    return fracs, accuracy


def plot_down_sampling(
    demuxEM_res_file: str, 
    out_file: str,
    probs: List[float] = [i / 10.0 for i in range(9, 0, -1)],
    n_threads: int = 1,
    dpi: int = 500,
    figsize: Tuple[float, float] = None,
):
    data = read_input(demuxEM_res_file)
    rna_gt = data.get_data(modality = "rna")
    hto_gt = data.get_data(modality = "hashing")

    fracs, accuracy = down_sampling(rna_gt, hto_gt, probs, n_threads=n_threads)

    plt.plot(fracs, accuracy, ".-")
    ax = plt.gca()
    ax.set_xlim(1.0, 0.0)
    ax.set_ylim(0.79, 1.01)
    vals = ax.get_yticks()
    ax.set_yticklabels(["{:.0%}".format(v) for v in vals])
    ax.set_xlabel("Fraction of hashtag UMIs")
    ax.set_ylabel("Consistency")
    if figsize is not None:
        plt.gcf().set_size_inches(*figsize)
    plt.savefig(out_file, dpi=dpi)
    plt.close()
