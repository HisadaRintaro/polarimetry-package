from matplotlib.colors import Normalize
from typing import cast
import matplotlib.pyplot as plt
from .base import setup_ax, add_colorbar
from .util import make_grid, plot_line
from ..models.area import RectangleArea
from .util import get_norm


def plot_stokes_para(
    image,
    *,
    area: RectangleArea | None = None,
    ax=None,
    stretch="asinh",
    vmin=None,
    vmax=None,
    title="",
):
    ax = setup_ax(ax)

    norm = get_norm(stretch, vmin=vmin, vmax=vmax)

    if type(area) == RectangleArea:
        mask = area.make_mask(image.shape)
        image = image[mask].reshape(area.shape())

    im = ax.imshow(image, norm=cast(Normalize,norm), cmap="gray")
    ax.set_title(f"Stokes {title}")
    add_colorbar(im, ax)

    return ax

def show_stokes_panel(
        I,
        Q,
        U,
        *,
        area: RectangleArea | None = None,
        axes = None,
        figsize= (15,4),
        stretchs: tuple = ("log", "asinh","asinh"),
        vmins: tuple = (None, None, None),
        vmaxs: tuple = (None, None, None),
        ):
        
    images = {"I":I, "Q":Q, "U":U}
    if axes is None:
        _, axes = plt.subplots(1,3, figsize=figsize)
    
    n = 0
    for name, image in images.items():
        plot_stokes_para(
                image,
                area=area,
                ax=axes[n],
                stretch=stretchs[n],
                vmin=vmins[n],
                vmax=vmaxs[n],
                title=name,
                )
        n += 1
    return axes

def plot_position_angle(
    back_image,
    position_angle,
    length,
    *,
    area: RectangleArea | None = None,
    ax=None,
    stretch="asinh",
    vmin=None,
    vmax=None,
    c= "white",
    linewidth= 1,
    **kwargs,
    ):

    ax = plot_stokes_para(
            back_image,
            area= area,
            ax= ax,
            stretch= stretch,
            vmin= vmin,
            vmax= vmax,
            )

    mx, my = make_grid(position_angle.shape)
    ax = plot_line(
            mx * length,
            my * length,
            position_angle,
            length = length,
            ax = ax,
            c= c,
            linewidth= linewidth,
            **kwargs,
            )
    return ax




