from abc import ABC, abstractmethod
from typing import Literal, cast
import numpy as np
from matplotlib.colors import Normalize
from ..area import RectangleArea
from ...plotting.util import get_norm


class ImagePlotMixin(ABC):
    @abstractmethod
    def _get_image(self, kind: Literal["image", "noise"], key: str) -> np.ndarray:
        pass

    def plot(
        self,
        *,
        kind: Literal["image", "noise"] = "image",
        key: str = "POL0",
        area: RectangleArea | None = None,
        ax=None,
        cmap="Grays",
        norm="log",
        vmin=None,
        vmax=None,
        title=None,
        colorbar=True,
        **kwargs,
    ):
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots()

        img = self._get_image(kind, key)
        if type(area) == RectangleArea:
            mask = area.make_mask(img.shape)
            img = img[mask].reshape(area.shape())

        norm = get_norm(norm, vmin=vmin, vmax=vmax)
        im = ax.imshow(img, cmap=cmap, norm=cast(Normalize,norm), **kwargs)

        if title:
            ax.set_title(title)
        if colorbar:
            plt.colorbar(im, ax=ax)

        return ax
