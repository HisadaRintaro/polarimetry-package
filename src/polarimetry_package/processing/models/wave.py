from dataclasses import dataclass
import numpy as np

@dataclass
class Wave:
    wave_min: float
    wave_max: float
    wave_len: int

    def array(self) -> np.ndarray:
        return np.linspace(self.wave_min, self.wave_max, self.wave_len)

    def differential(self) -> float:
        return (self.wave_max - self.wave_min) / self.wave_len
