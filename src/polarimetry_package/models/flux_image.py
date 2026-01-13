from dataclasses import dataclass, replace
import numpy as np
from typing import Self, Literal
from .image_set import ImageSet
from .header import HeaderProfile
from .mixin.plot_mixin import ImagePlotMixin
from .mixin.noise_mixin import NoiseMixin
from ..processing import flux

@dataclass(frozen=True)
class FluxImage(ImagePlotMixin, NoiseMixin):
    flux: dict[str, np.ndarray]
    noise: dict[str, np.ndarray]
    unit: str
    photflam: dict[str, float]
    exptime: dict[str, float]
    hdr_profile: HeaderProfile

    def __repr__(self) -> str:
        keys = list(self.flux.keys())
        shapes = {
            k: (None if v is None else v.shape)
            for k, v in self.flux.items()
        }
        return (
            f"FluxImage("
            f"keys={keys},\n "
            f"shapes={shapes},\n "
            f"unit={self.unit}\n "
            f")"
        )

    @classmethod
    def load(cls, image_set: ImageSet) -> Self:
        if image_set.status.get("binning", True) != "COMPLETE":
            raise RuntimeError(
                    "load() requires 'binning' = 'COMPLETE'"
                    )
        if image_set.noise is None:
            raise ValueError("noise is None")
        flux_image: dict[str, np.ndarray] = {}
        noise_image: dict[str, np.ndarray] = {}
        exptimes: dict[str, float] = {}
        photflams: dict[str, float] = {}
        for pol, data in image_set.data.items():
            exptime = image_set.hdr_profile.exptime(pol)
            photflam = image_set.hdr_profile.photflam(pol)
            polarizer_noise = image_set.noise[pol]
            flux_image[pol] = flux.to_flux(data, exptime, photflam, unit= "count")
            if polarizer_noise is None: raise ValueError("polarizer_noise is None")
            noise_image[pol] = flux.to_flux(polarizer_noise.cal_noise(), exptime, photflam, unit="count")
            exptimes[pol] = exptime
            photflams[pol] = photflam

        return cls(
                flux= flux_image,
                noise= noise_image,
                unit = "erg/s/cm-2/Å",
                exptime= exptimes,
                photflam= photflams, 
                hdr_profile= image_set.hdr_profile,
                )
        
    def to_flux(self) -> Self:
        return replace(self,
                flux= {pol: flux.to_flux(self.flux[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.flux.items()},
                noise= {pol: flux.to_flux(self.noise[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.noise.items()},
                unit= "erg/s/cm-2/Å",
                )

    def to_count_rate(self) -> Self:
        return replace(self,
                flux= {pol: flux.to_count_rate(self.flux[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.flux.items()},
                noise= {pol: flux.to_count_rate(self.noise[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.noise.items()},
                unit= "count/s",
                )

    def to_count(self) -> Self:
        return replace(self,
                flux= {pol: flux.to_count(self.flux[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.flux.items()},
                noise= {pol: flux.to_count(self.noise[pol],
                                         self.exptime[pol],
                                         self.photflam[pol],
                                         self.unit)
                       for pol, _ in self.noise.items()},
                unit= "count",
                )
    
    def _get_image(self, kind: Literal["image", "noise"], key: str) -> np.ndarray:
        if kind == "image":
            return self.flux[key]
        elif kind == "noise":
            return self.noise[key]
        
