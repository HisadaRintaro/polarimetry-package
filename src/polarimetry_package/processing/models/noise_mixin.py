from abc import ABC, abstractmethod
from typing import Literal
import numpy as np
from .area import RectangleArea

class NoiseMixin(ABC):
    @abstractmethod
    def _get_image(self, kind: Literal["image", "noise"], key: str) -> np.ndarray:
        pass

    def SN(
        self,
        key: str = "POL0",
        ) -> np.ndarray:

        image = self._get_image("image", key)
        noise = self._get_image("noise", key)
        return image / noise

    def make_mask(
        self,
        key: str = "POL0",
        ratio= 3,
        ) -> np.ndarray:

        sn_img = self.SN(key)
        return sn_img > ratio
        
    def plot_SN(
        self,
        *,
        key: str = "POL",
        area: RectangleArea | None = None,
        ax= None,
        cmap = "Grays",
        norm= None,
        title= None,
        colorbar= True,
        **kwargs,
        ):
        import matplotlib.pyplot as plt

        if ax is None:
            _, ax = plt.subplots()

        sn_img = self.SN(key)
        if type(area) == RectangleArea:
            mask = area.make_mask(sn_img.shape)
            sn_img = sn_img[mask].reshape(area.shape())
        im = ax.imshow(sn_img, cmap=cmap, norm=norm, **kwargs)

        if title:
            ax.set_title(title)
        if colorbar:
            plt.colorbar(im, ax=ax)

        return ax

