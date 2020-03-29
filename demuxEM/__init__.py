from .demuxEM import estimate_background_probs, demultiplex
from .plot import (
    plot_adt_hist,
    plot_rna_hist,
    plot_bar,
    plot_violin,
    plot_heatmap,
    plot_dataframe_bar,
)
from .down_sampling import plot_down_sampling

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
