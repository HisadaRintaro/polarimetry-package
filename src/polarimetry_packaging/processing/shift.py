import numpy as np


def crosscorr2d(pix1, pix2):
  """
    Take cross correlation of two 2D images.

    Inputs: pix1, pix2 ... two 2D images
    Output: cross correlation 2D image (complex numbers)

  """
  return np.fft.fftshift(np.fft.ifft2( \
    np.fft.fft2(pix1).conj() * np.fft.fft2(pix2) ))

def find_shift(pix1, pix2):
  """
    Find shift of pix2, with respect to pix1.

    Inputs: pix1, pix2 ... two 2D images (real numbers)
    Output: a tuple of (yshift, xshift) 
            ... pix2 is shifted by (yshift,xshift) from pix1

  """
  cc = np.real(crosscorr2d(pix1, pix2))
  ypeak,xpeak = np.unravel_index(cc.argmax(), cc.shape)
  return ypeak-cc.shape[0]/2, xpeak-cc.shape[1]/2
