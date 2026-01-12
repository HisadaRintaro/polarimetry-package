from dataclasses import dataclass
from typing import Self
from .transmittance import Transmittance, Wave
from .header import HeaderRaw

@dataclass
class PolarrizationEfficiency:
    major: Transmittance
    minor: Transmittance

    @classmethod
    def load(cls, header_raw: HeaderRaw) -> Self:
        major = Transmittance.load(header_raw, orientation= "par")
        minor = Transmittance.load(header_raw, orientation= "per")
        return cls(
                major= major,
                minor= minor,
                )

    def k(self, wave: Wave) -> float:
        t_major = self.major.trans_mean(wave)
        t_minor = self.minor.trans_mean(wave)
        return (t_major - t_minor) / (t_major + t_minor)

