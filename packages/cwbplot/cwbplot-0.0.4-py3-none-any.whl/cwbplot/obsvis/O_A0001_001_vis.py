from datetime import datetime
from cwbplot import cwb_colorbar
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

dicts = {"TEMP":"Temperature ($^\circ$C)"}



def O_A0001_VIS(pdf, metvars, cut = False):
    lat = pdf["lat"].astype(float).values
    lon = pdf["lon"].astype(float).values
    mets = pdf[metvars].astype(float).values
    obstime = pdf["time"]
    fig = plt.figure(figsize=(16,12))
    if cut:
        if isinstance(cut,tuple) or isinstance(cut,list):
            lllon, urlon, lllat, urlat = cut[0], cut[1], cut[2], cut[3]
        else:
            lllon, urlon, lllat, urlat = 117.5, 122.5, 21.5, 26
    else:
        lllon, urlon, lllat, urlat = 117.5, 122.5, 21.5, 26
    m = Basemap(projection='merc',resolution="f",
               llcrnrlon=lllon, llcrnrlat=lllat,
               urcrnrlon=urlon, urcrnrlat=urlat)
    m.drawcoastlines()
    if metvars == "TEMP":
        surfT = cwb_colorbar.surfT()
        sct = m.scatter(lon, lat, c = mets, cmap = surfT["cmap"], norm=surfT["norm"], latlon=True)
    else:
        sct = m.scatter(lon, lat, c = mets )
    cbar = plt.colorbar(sct)
    cbar.set_label(dicts[metvars], size=14)
    plt.title(obstime[0],fontsize=18)
    return fig, m
