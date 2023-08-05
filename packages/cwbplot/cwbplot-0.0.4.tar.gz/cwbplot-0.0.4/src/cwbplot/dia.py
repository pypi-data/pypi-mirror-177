import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def perform_dig(figobj, subplot = False,bais_color="red",csi_cmap="Blues"):
     grid_ticks = np.arange(0, 1.01, 0.001)
     sr_g, pod_g = np.meshgrid(grid_ticks, grid_ticks)
     bias = pod_g / sr_g
     csi = 1.0 / (1.0 / sr_g + 1.0 / pod_g - 1.0)
     if int(subplot) == 0:
         try:
             if len(figobj.axes) == 0:
                 digbg = figobj.subplots(1)
         except:
             digbg = figobj
     else:
         try:
             if len(figobj.axes) == 0:
                 digbg = figobj.subplots(1)
         except:
             digbg = figobj
     csi_contour = digbg.contourf(sr_g, pod_g, csi, np.arange(0.1, 1.1,0.1), extend="max", cmap=csi_cmap)
     b_contour = digbg.contour(sr_g, pod_g, bias, [0.1, 0.2, 0.5, 1, 2,5, 10], colors="slateblue", linestyles="dashed")
     ax2ticks = [0.1,0.2,0.5,1]
     ax2tickslabel = [1/x for x in ax2ticks]
     secax = digbg.secondary_xaxis('top')
     secay = digbg.secondary_yaxis('right')
     secax.set_xticks(ax2ticks)
     secax.set_xticklabels(ax2tickslabel, minor=False)
     plt.colorbar(csi_contour,ax=digbg)
     digbg.set_xlim(0,1)
     digbg.set_ylim(0,1)
     return digbg
