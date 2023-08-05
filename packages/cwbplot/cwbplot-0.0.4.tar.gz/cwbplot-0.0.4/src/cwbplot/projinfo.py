from mpl_toolkits.basemap import Basemap
import pandas as pd
import cwbplot

pp = cwbplot.__path__[0]
forlcc = pd.read_csv("{}/lcc.csv".format(pp),index_col=[0])

def wrfd(lon, lat,  domain, projection= 'lcc', res="l", cut = False, center =False, ax=False):
    idx = "WRFM04"+domain
    lon0, lat0 = forlcc.loc[idx]["lon0"], forlcc.loc[idx]["lat0"]
    lat1, lat2 = forlcc.loc[idx]["lat1"], forlcc.loc[idx]["lat2"]
    if cut == False and projection == 'lcc' and center == False:
        if ax == False:
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = lat[0,0],
                    llcrnrlon = lon[0,0],
                    urcrnrlat = lat[-1,-1],
                    urcrnrlon = lon[-1,-1])
        else:
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = lat[0,0],
                    llcrnrlon = lon[0,0],
                    urcrnrlat = lat[-1,-1],
                    urcrnrlon = lon[-1,-1], ax = ax)
    elif isinstance(cut,tuple) or isinstance(cut,list) and projection == "lcc" and center==False:
        if len(cut) == 4:
            if ax == False:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
            else:
                 wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1], ax= ax)
        else:
            print("Object cut length must 4")
    elif not isinstance(cut,tuple) and not isinstance(cut,list) and projection == "lcc" and center==False:
        print("Object cut type must tuple or list")
    
    if cut == False and projection == 'cyl':
        if center == False:
            if ax == False:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0,
                    llcrnrlat = lat.min(),
                    llcrnrlon = lon.min(),
                    urcrnrlat = lat.max(),
                    urcrnrlon = lon.max())
            else:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0,
                    llcrnrlat = lat.min(),
                    llcrnrlon = lon.min(),
                    urcrnrlat = lat.max(),
                    urcrnrlon = lon.max(), ax = ax)
        if isinstance(center,tuple) or isinstance(center,list):
            if ax == False:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = center[0], lat_0 = center[1])
            else:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = center[0], lat_0 = center[1], ax= ax)
        elif isinstance(center,tuple) and isinstance(center,list):
            print("Object center must tuple or list and length must 2")
    elif isinstance(cut,tuple) or isinstance(cut,list) and projection == "cyl":
        if center == False:
            if ax == False:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 , 
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
            else:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 ,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1], ax= ax)
        if isinstance(center,tuple) or isinstance(center,list):
            if ax == False:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 ,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
            else:
                wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 ,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1], ax= ax)
        elif isinstance(center,tuple) and isinstance(center,list):
            print("Object center must tuple or list and length must 2")
    elif cut and projeciotn == "cyl":
        if isinstance(cut,tuple) and isinstance(cut,list):
            print("Object cut type must tuple or list")
    
    return wrfproj


def rwrf(lon, lat,  domain="d01", projection= 'lcc', res="l", cut = False, center =False):
    idx = "RWRFM01"+domain
    lon0, lat0 = forlcc.loc[idx]["lon0"], forlcc.loc[idx]["lat0"]
    lat1, lat2 = forlcc.loc[idx]["lat1"], forlcc.loc[idx]["lat2"]
    if cut == False and projection == 'lcc' and center == False:
        wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = lat[0,0],
                    llcrnrlon = lon[0,0],
                    urcrnrlat = lat[-1,-1],
                    urcrnrlon = lon[-1,-1])
    elif isinstance(cut,tuple) or isinstance(cut,list) and projection == "lcc" and center==False:
        if len(cut) == 4:
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0, lat_1 = lat1, lat_2 = lat2,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
        else:
            print("Object cut length must 4")
    elif not isinstance(cut,tuple) and not isinstance(cut,list) and projection == "lcc" and center==False:
        print("Object cut type must tuple or list")
    
    if cut == False and projection == 'cyl':
        if center == False:
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 = lat0,
                    llcrnrlat = lat.min(),
                    llcrnrlon = lon.min(),
                    urcrnrlat = lat.max(),
                    urcrnrlon = lon.max())
        if isinstance(center,tuple) or isinstance(center,list):
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = center[0], lat_0 = center[1])
        elif isinstance(center,tuple) and isinstance(center,list):
            print("Object center must tuple or list and length must 2")
    elif isinstance(cut,tuple) or isinstance(cut,list) and projection == "cyl":
        if center == False:
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 ,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
        if isinstance(center,tuple) or isinstance(center,list):
            wrfproj = Basemap(projection=projection, resolution = res, rsphere = 6370000. ,
                    lon_0 = lon0, lat_0 =lat0 ,
                    llcrnrlat = cut[2],
                    llcrnrlon = cut[0],
                    urcrnrlat = cut[3],
                    urcrnrlon = cut[1])
        elif isinstance(center,tuple) and isinstance(center,list):
            print("Object center must tuple or list and length must 2")
    elif cut and projeciotn == "cyl":
        if isinstance(cut,tuple) and isinstance(cut,list):
            print("Object cut type must tuple or list")
    return wrfproj
