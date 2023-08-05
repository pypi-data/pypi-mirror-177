import requests
import pandas as pd
from datetime import datetime

#2022-11-09 11:00:00
def apiget(api=False):
    if api == False:
        print("Plz give the path for api readable")
    else:
        with open(api,"r") as myapi:
            apiapi = myapi.read().rstrip("\n")
    dataid="O-A0003-001"
    dformat="json"
    url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{dataid}?Authorization={apiapi}&format={dformat}"
    r = requests.get(url)
    fn = r.json()
    collout = []
    for stn in range(len(fn["records"]["location"])):
        dicts =  fn["records"]["location"][0].keys()
        coll = []
        header = []
        for dic in dicts:
            fndict = fn["records"]["location"][stn][dic]
            if dic == "time":
                header.append(dic)
                timedict = fndict['obsTime']
                coll.append(datetime.strptime(timedict,"%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H"))
            elif dic != "weatherElement" and dic != "parameter" and dic != "time":
                header.append(dic)
                coll.append(fndict)
            elif dic == "weatherElement":
                for element in range(len(fndict)):
                    header.append(fndict[element]["elementName"])
                    coll.append(fndict[element]["elementValue"])
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
    #fn = jsonf["records"]["location"]
    return finaldf

#["records"]["location"][0]
