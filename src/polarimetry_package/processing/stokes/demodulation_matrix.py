from dataclasses import dataclass
from typing import Self
import numpy as np
from .polarization_efficiency import PolarrizationEfficiency
from ..models.header import HeaderProfile
from ..models.wave import Wave


@dataclass
class DemodulationMatrixFactory:
    polarization_eff: dict[str, PolarrizationEfficiency]
    wave: Wave

    @classmethod
    def load(cls, header_profile: HeaderProfile, wave: Wave) -> Self:
        pol_eff: dict[str, PolarrizationEfficiency] = {}
        for pol, header_raw in header_profile.raw.items():
            pol_eff[pol] = PolarrizationEfficiency.load(header_raw)
        return cls(
                polarization_eff = pol_eff,
                wave = wave,
                )

    def matrix(self) -> np.ndarray:
        k1 = self.polarization_eff["POL0"].k(self.wave); theta1 = 0
        k2 = self.polarization_eff["POL60"].k(self.wave) ; theta2 = np.pi * 1/3
        k3 = self.polarization_eff["POL120"].k(self.wave) ; theta3 = np.pi * 2/3

        a = k2* k3* np.sin(-2*theta2 + 2*theta3)\
                + k3* k1* np.sin(-2*theta3 + 2*theta1)\
                + k1* k2* np.sin(-2*theta1 + 2* theta2)

        a1_1 =  k2* k3* np.sin(-2*theta2 + 2*theta3)
        a2_1 = -k2* np.sin(2*theta2) + k3* np.sin(2*theta3)
        a3_1 =  k2* np.cos(2*theta2) - k3* np.cos(2*theta3)
        
        a1_2 =  k3* k1* np.sin(-2*theta3 + 2*theta1)
        a2_2 = -k3* np.sin(2*theta3) + k1* np.sin(2*theta1)
        a3_2 =  k3* np.cos(2*theta3) - k1* np.cos(2*theta1)

        a1_3 =  k1* k2* np.sin(-2*theta1 + 2*theta2)
        a2_3 = -k1* np.sin(2*theta1) + k2* np.sin(2*theta2)
        a3_3 =  k1* np.cos(2*theta1) - k2* np.cos(2*theta2)

        mueller_matrix = 1/a * np.array([[a1_1,a1_2,a1_3],
                                         [a2_1,a2_2,a2_3],
                                         [a3_1,a3_2,a3_3]])
        return mueller_matrix
    
#plotting/stokes_plottingへ移植済み（2026.1.14）
#    def plot_transmittance_curve(self, wave: Wave, ax= None, ymax=1, **kwargs):
#        ax = setup_ax(ax)
#
#        for pol, pol_eff in self.polarization_eff.items():
#            ax = pol_eff.major.plot_curve(wave, label= f"{pol}_major", ax=ax, ymax=ymax, **kwargs)
#            ax = pol_eff.minor.plot_curve(wave, label= f"{pol}_minor", ax=ax, ymax=ymax, **kwargs)
#
#        ax.set_xlabel("$wave length [ \\AA ]$")
#        ax.set_ylabel("transmittance")
#        ax.legend()
#        ax.grid(True)
#        return ax
