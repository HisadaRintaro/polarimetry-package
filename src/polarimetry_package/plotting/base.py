import matplotlib.pyplot as plt

def setup_ax(ax=None, figsize=(5, 4)):
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
    return ax

def add_colorbar(im, ax):
    plt.colorbar(im, ax=ax)
