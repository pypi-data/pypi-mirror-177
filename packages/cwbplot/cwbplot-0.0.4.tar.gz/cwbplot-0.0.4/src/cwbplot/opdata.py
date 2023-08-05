import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import json
import pygrib as pb
import matplotlib.pyplot as plt
from datetime import datetime
from cwbplot.json import *
from cwbplot.obsvis import *
from cwbplot import cwb_colorbar
from mpl_toolkits.basemap import Basemap

try:
    from osgeo import gdal
except:
    print("Gdal package can't be imported, which probably not be installed")
    print("Function for read geotiff data can't be used")



def judecat(idname):
    if "_" in idname:
        splitidx = idname.split("_")
        if "CWB" in splitidx:
            splitidx.remove("CWB")
    elif "-" in idname:
        splitidx = idname.split("-")
    lengstr = [ len(xx) for xx in splitidx ]
    if len(lengstr) <= 1:
        idxmainstr = splitidx[lengstr.index(max(lengstr))]
        idxsubstr = False
    elif len(lengstr) > 1:
        idxmainstr = splitidx[lengstr.index(max(lengstr))]
        idxsubstr = splitidx[lengstr.index(3)]
    return idxmainstr, idxsubstr

def onestn(lociter, elements):
    """
    lociter代表針對根的location的iter，即roots.iter("{urn:cwb:gov:tw:cwbcommon:0.1}location")
    以此份資料來說，一個location代表一個測站。
    elements代表location的該層資訊及下一層標記。
    """
    valu, header = [],[]  #儲存數值及檔頭用
    cnt = 1
    itercol = [ lociter.iter(eachtag) for eachtag in elements] #先對每個element進行iter
    
    for eachiter, eachelement in zip(itercol,elements):
        for elements in eachiter:
            if "weatherElement" not in eachelement and "parameter" not in eachelement and "time" not in eachelement:
                header.append(eachelement.split("}")[-1])
                valu.append(elements.text)
            else:
                for qqinin in elements:
                    if  "weatherElement" in eachelement:
                        for xxin in qqinin.iter("{urn:cwb:gov:tw:cwbcommon:0.1}elementName"):
                            if cnt == 1:                            
                                header.append(xxin.text)
                        for xxin in qqinin.iter("{urn:cwb:gov:tw:cwbcommon:0.1}elementValue"):
                            valu.append(xxin[0].text)
                    elif "parameter" in eachelement:
                        for xxin in qqinin.iter("{urn:cwb:gov:tw:cwbcommon:0.1}parameterName"):
                            if cnt ==1:
                                header.append(xxin.text)
                        for xxin in qqinin.iter("{urn:cwb:gov:tw:cwbcommon:0.1}parameterValue"):
                            valu.append(xxin.text)
                    else:
                        header.append(eachelement.split("}")[-1])
                        obst = datetime.strptime(qqinin.text,"%Y-%m-%dT%H:%M:%S+08:00").strftime("%Y%m%d%H")
                        valu.append(obst)
    cnt = 2
    return header, valu

def radarcomp(fn_roots,catgo):
    if catgo == "xml":
        for qq in fn_roots.iter("{urn:cwb:gov:tw:cwbcommon:0.1}dataset"):
            for qqqq in qq:
                if "contents" in qqqq.tag.split("}"):
                    rdecho = qqqq[1].text.split(",")
                    floatradar = [ float(xx) for xx in rdecho]
        for qq in fn_roots.iter("{urn:cwb:gov:tw:cwbcommon:0.1}parameter"):
            if qq[0].text == "左下角":
                lonstr, latstr = qq[1].text.split(",")
                startlon, startlat = float(lonstr), float(latstr)
            if qq[0].text == "時間":
                obstime = datetime.strptime(qq[1].text,"%Y-%m-%dT%H:%M:%S+08:00").strftime("%Y%m%d%H")
            if qq[0].text == "解析度":
                resolution = float(qq[1].text)
            if qq[0].text == "維度(nx*ny)":
                xgridstr, ygridstr = qq[1].text.split("*")
                xgrid, ygrid = int(xgridstr), int(ygridstr)
    elif catgo == "json":
        rdecho = fn_roots["cwbopendata"]["dataset"]["contents"]["content"].split(",")
        floatradar = [ float(xx) for xx in rdecho]
        for qq in fn_roots["cwbopendata"]["dataset"]["datasetInfo"]["parameterSet"]["parameter"]:
            if qq["parameterName"] == "左下角":
                lonstr, latstr = list(qq.values())[1].split(",")
                startlon, startlat = float(lonstr), float(latstr)
            if qq["parameterName"] == "時間":
                obstime = datetime.strptime(list(qq.values())[1],"%Y-%m-%dT%H:%M:%S+08:00").strftime("%Y%m%d%H")
            if qq["parameterName"] == "解析度":
                resolution = float(list(qq.values())[1])
            if qq["parameterName"] == "維度(nx*ny)":
                xgridstr, ygridstr = list(qq.values())[1].split("*")
                xgrid, ygrid = int(xgridstr), int(ygridstr)
    lonx = np.linspace(startlon, startlon+resolution*(xgrid-1), xgrid)
    laty = np.linspace(startlat, startlat+resolution*(ygrid-1), ygrid)
    lon, lat = np.meshgrid(lonx, laty)
    radar = np.array(floatradar).reshape(ygrid,xgrid)
    return radar, lon, lat, obstime

def gtiff(fn,infolatlon):
    sattif = gdal.Open(fn,gdal.GA_ReadOnly)
    data  = sattif.GetRasterBand(1) #取值
    data2arr = data.ReadAsArray() #僵值轉換為array
    albdo = data2arr/1000.
    llx, pixelx, skx, lly, sky, pixely = sattif.GetGeoTransform()
    lrx = llx + (sattif.RasterXSize * pixelx)
    lry = lly + (sattif.RasterYSize* pixely)
    return albdo, infolatlon

def read_xml(fn,tiff_fn=False):
    trees = ET.parse(fn)
    roots = trees.getroot()
    ids = next(roots.iter("{urn:cwb:gov:tw:cwbcommon:0.1}dataid")).text
    maincat, subcat = judecat(ids)
    if maincat == "A0001" or maincat=="A0002" or maincat == "A0003":
        loc_element = ['{urn:cwb:gov:tw:cwbcommon:0.1}time',
               '{urn:cwb:gov:tw:cwbcommon:0.1}stationId',
               '{urn:cwb:gov:tw:cwbcommon:0.1}locationName',
               '{urn:cwb:gov:tw:cwbcommon:0.1}lon',
               '{urn:cwb:gov:tw:cwbcommon:0.1}lat',
               '{urn:cwb:gov:tw:cwbcommon:0.1}lon_wgs84',
               '{urn:cwb:gov:tw:cwbcommon:0.1}lat_wgs84',
               '{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement',
               '{urn:cwb:gov:tw:cwbcommon:0.1}parameter',
              ]
        packvalue = []
        for qq in roots.iter("{urn:cwb:gov:tw:cwbcommon:0.1}location"):
            ch, eachvalue = onestn(qq, loc_element)
            packvalue.append(eachvalue)
        xml2df = pd.DataFrame(packvalue,columns=ch)
        dfORarr = xml2df       
    elif maincat == "A0059":
        radararr = radarcomp(roots, catgo="xml")
        dfORarr = radararr
    elif maincat == "B0056":
        if tiff_fn == False:
            print("Plz give geotiff filename with path")
        else:
            lonlatlist = []
            for lonlat in roots.iter('{urn:cwb:gov:tw:cwbcommon:0.1}parameterValue'):
                limt_l, limt_r = lonlat.text.split(" - ")
                lonlatlist.append(float(limt_l))
                lonlatlist.append(float(limt_r))
            sat = gtiff(tiff_fn, lonlatlist)
            dfORarr = sat
    return dfORarr

def read_json(fn):
    with open(fn,"r",encoding='utf-8') as jj:
        fn = json.load(jj)
    ids = fn["cwbopendata"]["dataid"]
    maincat, subcat = judecat(ids)
    if maincat == "A0001" or maincat == "A0002" or maincat =="A0003":
        collout = []
        for stn in range(len(fn["cwbopendata"]["location"])):
            dicts =  fn["cwbopendata"]["location"][0].keys()
            coll = []
            header = []
            for dic in dicts:        
                fndict = fn["cwbopendata"]["location"][stn][dic]
                if dic == "time":
                    header.append(dic)
                    timedict = fndict['obsTime']
                    coll.append(datetime.strptime(timedict,"%Y-%m-%dT%H:%M:%S+08:00").strftime("%Y%m%d%H"))
                elif dic != "weatherElement" and dic != "parameter" and dic != "time":
                    header.append(dic)
                    coll.append(fndict)
                elif dic == "weatherElement":
                    for element in range(len(fndict)):
                        header.append(fndict[element]["elementName"])
                        coll.append(fndict[element]["elementValue"]["value"])
                elif dic == "parameter":
                    for parame in range(len(fndict)):
                        header.append(fndict[parame]["parameterName"])
                        coll.append(fndict[parame]["parameterValue"])
            collout.append(coll)
            df = pd.DataFrame(collout, columns = header)
            header.remove("time")
            header.insert(0,"time")
            finaldf = df.loc[:,header]
            dfORarr = finaldf
    elif maincat == "A0059":
        radararr = radarcomp(fn, catgo="json")
        dfORarr = radararr
    return dfORarr

def draw(fn=False,types=False, apipath=False, cut=False, metvars=False):
    if fn and not apipath:
        with open(fn,"r",encoding='utf-8') as jj:
            fn = json.load(jj)
        ids = fn["cwbopendata"]["dataid"]
        maincat, subcat = judecat(ids)
    else:
        maincat = False
    if maincat == "A0059":
        fig = plt.figure()
        radar, lon, lat, obstime = radarcomp(fn, catgo="json")
        radar[radar == -99.] = np.nan
        radarcm = cwb_colorbar.radar()
        projs = Basemap(projection='merc',resolution="l",urcrnrlat=lat[-1,-1], llcrnrlat=lat[0,0], llcrnrlon=lon[0,0], urcrnrlon=lon[-1,-1])
        projs.drawcoastlines()
        if types == "scatter":
            sct = projs.scatter(lon, lat, c=radar, cmap = radarcm["cmap"], norm=radarcm["norm"], latlon=True)
        elif types == "imshow":
            sct = projs.imshow(radar,cmap = radarcm["cmap"], norm=radarcm["norm"],extent=(lon[0,0],lon[1,1],lat[-1,-1],lat[0,0]))
        elif types == "contourf":
            sct = projs.contourf(lon, lat,radar, cmap = radarcm["cmap"], norm=radarcm["norm"], levels = radarcm["levels"],latlon=True)
        plt.colorbar(sct)
        plt.title(obstime,fontsize=18)
    if maincat == "A0001" or fn == "O-A0001-001":
        outfn = O_A0001_001.apiget(apipath)
        fig, projs = O_A0001_001_vis.O_A0001_VIS(outfn, metvars)
    return fig, projs

def json_api(fn,apipath):
    if fn == "O-A0001-001":
       outfn = O_A0001_001.apiget(apipath)
    elif fn == "O-A0002-001":
       outfn = O_A0002_001.apiget(apipath)
    elif fn == "O-A0003-001":
       outfn = O_A0003_001.apiget(apipath)
    return outfn

def read_grib(fn):
    outfn = pb.open(fn)
    return outfn
