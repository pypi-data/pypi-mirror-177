import math
import random as rand
from typing import Optional

import numpy as np
from anndata import AnnData
from tqdm.notebook import tqdm


def randomize_positions(
    adata: AnnData, radius: float, progress_bar: Optional[bool] = False, return_positions: Optional[bool] = False
) -> Optional[np.ndarray]:
    """Randomizes positions within a given radius.

    Parameters
    ----------
    adata
        Annotated data matrix. Coordinates are taken from `adata.obsm["X_spatial"]`.
    radius
        Radius to randomize within. Measured in same units as coordinates.
    progress_bar
        Whether to show a progress bar.
    return_positions
        Whether to return the randomized positions or assign them to
        `adata.obsm["X_spatial_random"]`.

    Returns
    -------
    If `return_positions = True`, returns a list of the randomized coordinates corresponding to
    the coordinates in `adata.obsm["X_spatial"]`. Otherwise, these coordinates are assigned to
    `adata.obsm["X_spatial_random"]`.
    """
    # Assign progress bar if input
    bar = lambda x: x
    if progress_bar:
        bar = tqdm
    # Initialize array with deltas to apply to the real coordinates
    transformations = np.empty((adata.shape[0], 2))
    for i in bar(range(adata.shape[0])):
        transformations[i] = [math.sin(math.pi * rand.random()) * radius, math.cos(math.pi * rand.random()) * radius]
    # Apply transformations to real coordinates (numpy does this element-wise)
    if return_positions:
        return transformations + adata.obsm["X_spatial"]
    else:
        adata.obsm["X_spatial_random"] = transformations + adata.obsm["X_spatial"]
