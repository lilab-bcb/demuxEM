import numpy as np

from scipy.sparse import issparse
from anndata import AnnData

def log_norm(data: AnnData, norm_count: float = 1e5) -> None:
    assert issparse(data.X)
    mat = data.X[:, data.var["robust"].values]
    scale = norm_count / mat.sum(axis=1).A1
    data.X.data *= np.repeat(scale, np.diff(data.X.indptr))
    data.X = data.X.log1p()