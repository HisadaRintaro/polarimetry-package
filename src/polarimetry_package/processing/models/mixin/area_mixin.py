#from abc import ABC, abstractmethod
#from matplotlib.patches import Patch
#
#class AreaPlotMixin(ABC):
#
#    @abstractmethod
#    def to_patch(self, **kwargs) -> Patch:
#        "return matplotlib patch"
#        pass
#
#    def plot_region(
#            self,
#            ax = None,
#            *,
#            color= "red",
#            linewidth = 2,
#            alpha = 1.0,
#            **kwargs,
#            ):
#        import matplotlib.pyplot as plt
#
#        if ax is None:
#            _, ax = plt.subplots()
#
#        patch = self.to_patch(
#                edgecolor = color,
#                linewidth = linewidth,
#                alpha = alpha,
#                **kwargs,
#                )
#        ax.add_patch(patch)
#        return ax
#
