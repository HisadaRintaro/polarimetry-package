from typing import Any
import numpy as np
from dataclasses import dataclass
from ..image.binning import binning_image

@dataclass
class Noise:
    count_noise: np.ndarray | None
    background_noise: np.floating[Any] | None
    bin_size: int 

    def cal_noise(self):
        bin_size = self.bin_size
        if self.count_noise is None:
            raise ValueError("count_noise is None")
        if self.background_noise is None:
            raise ValueError("background_noise is None")

        return np.sqrt(
                binning_image(
                    self.count_noise**2, bin_size
                    ) + bin_size**2 * self.background_noise**2
                )
