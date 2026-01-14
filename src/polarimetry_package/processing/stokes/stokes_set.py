from dataclasses import dataclass
from typing import Self, Literal
import numpy as np

from ..flux.flux_image import FluxImage
from .demodulation_matrix import DemodulationMatrixFactory
from ...plotting.plot_mixin import ImagePlotMixin
from ..models.noise_mixin import NoiseMixin
from ..models.wave import Wave

@dataclass(frozen=True)
class StokesParameter(ImagePlotMixin, NoiseMixin):
    I: np.ndarray
    Q: np.ndarray
    U: np.ndarray
    noise_I: np.ndarray
    noise_Q: np.ndarray
    noise_U: np.ndarray

    def __repr__(self) -> str:
        shapes: set = {self.I.shape, self.Q.shape, self.U.shape, self.noise_I.shape, self.noise_Q.shape, self.noise_U.shape}
        return (
            f"StokesParameter(\n "
            f"keys= [I, Q, U, noise_I, noise_Q, noise_U],\n "
            f"shapes={shapes},\n "
            f")"
        )

    @staticmethod
    def apply_mueller_matrix(images: dict[str, np.ndarray], matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        f_stacked = np.stack([ image for _, image in images.items()]).reshape(3,-1)
        shapes = {v.shape for v in images.values()}
        I, Q, U = (matrix @ f_stacked).reshape(3, *list(shapes)[0])
        return I, Q, U
    
    @classmethod
    def load(cls, flux_image: FluxImage, wave: Wave) -> Self:
        mueller_matrix = DemodulationMatrixFactory.load(flux_image.hdr_profile, wave).matrix()
        I, Q, U = cls.apply_mueller_matrix(flux_image.flux, mueller_matrix)
        noise_I, noise_Q, noise_U = cls.apply_mueller_matrix(flux_image.noise, mueller_matrix)
        return cls(
                I= I,
                Q= Q,
                U= U,
                noise_I= noise_I,
                noise_Q= noise_Q,
                noise_U= noise_U,
                )
    def _get_image(self, kind: Literal["image", "noise"], key: str) -> np.ndarray:
        if key == "I" and kind == "image":
            return self.I
        elif key == "Q" and kind == "image":
            return self.Q
        elif key == "U" and kind == "image":
            return self.U
        elif key == "I" and kind == "noise":
            return self.noise_I
        elif key == "Q" and kind == "noise":
            return self.noise_Q
        elif key == "U" and kind == "noise":
            return self.noise_U
        else:
            raise ValueError(f"Unknown kind or key: {kind},{key}")

@dataclass
class PolarizationDegree(ImagePlotMixin, NoiseMixin):
    P: np.ndarray
    noise_P: np.ndarray

    def __repr__(self) -> str:
        shapes: set = {self.P.shape, self.noise_P.shape}
        return (
            f"PolarizationDegree(\n "
            f"keys= [P, noise_P],\n "
            f"shapes={shapes},\n "
            f")"
        )

    @staticmethod
    def cal_pola_deg(I, Q, U) -> np.ndarray:
        return np.sqrt(Q**2 + U**2) / I
    
    @staticmethod
    def cal_noise_pola_deg(I, noise_I) -> np.ndarray:
        return np.sqrt(2) * noise_I / I

    @classmethod
    def load(cls, stokes_para: StokesParameter) -> Self:
        P = cls.cal_pola_deg(
                stokes_para.I,
                stokes_para.Q,
                stokes_para.U
                )
        noise_P = cls.cal_noise_pola_deg(
                stokes_para.I,
                stokes_para.noise_I
                )
        return cls(
                P= P,
                noise_P= noise_P,
                )

    def _get_image(self, kind: Literal["image", "noise"], key: str="POL0") -> np.ndarray:
        if kind == "image":
            return self.P
        elif kind == "noise":
            return self.noise_P

@dataclass
class PositionAngle:
    theta: np.ndarray
    #noise_theta: np.ndarray
    #そのうち実装する

    def __repr__(self) -> str:
        shapes: set = {self.theta.shape}
        return (
            f"PositionAngle(\n "
            f"keys= [theta],\n "
            f"shapes={shapes},\n "
            f")"
        )

    @staticmethod
    def cal_position_angle(Q, U, mask: np.ndarray | None = None) -> np.ndarray:
        theta =  1/2 * np.arctan2(U,Q)
        if isinstance(mask, np.ndarray):
            theta[mask == False] = np.nan
        return theta


    @classmethod
    def load(cls, stokes_para: StokesParameter, mask = None) -> Self:
        theta = cls.cal_position_angle(
                stokes_para.Q,
                stokes_para.U,
                mask = mask,
                )
        return cls(
                theta= theta,
                )



