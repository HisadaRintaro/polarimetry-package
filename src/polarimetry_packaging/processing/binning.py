import numpy as np

def binning_image(image:np.ndarray | None, bin_size: int) -> np.ndarray:
    if image is None:
        raise ValueError("image is None")
    if image.ndim != 2:
        raise RuntimeError("The dimention of image must be 2.")
    ysize, xsize = image.shape
    mod_ysize, mod_xsize = np.mod((ysize, xsize), bin_size)
    trimed_image: np.ndarray = image[:-mod_ysize, :-mod_xsize]

    return (
            trimed_image
            .reshape(ysize//bin_size, bin_size, xsize//bin_size, bin_size)
            .sum(axis= (1, 3))
            )
