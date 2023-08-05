import matplotlib.colors as mcolors


def rain(colorlevel = [0,0.1,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400], style = 'nwprfs'):
    if style == "nwprfs":
        cwb_data=['None','#C6C5C3','#9BFFFF','#00CFFF','#0198FF','#0165FF','#309901','#32FF00','#F8FF00','#FFCB00',\
               '#FF9A00','#FA0300','#CC0003', '#A00000','#98009A','#C304CC','#F805F3','#FECBFF']
        cmaps = mcolors.ListedColormap(cwb_data,'precipitation')
        numticks = len(cwb_data) +1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [0,0.1,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]")
            colorlevel = [0,0.1,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    elif style.lower() == 'npd':
        colorlevelnpd = [0,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]
        cwb_data=['None','#9BFFFF','#00CFFF','#0198FF','#0165FF','#309901','#32FF00','#F8FF00','#FFCB00',\
               '#FF9A00','#FA0300','#CC0003', '#A00000','#98009A','#C304CC','#F805F3','#FECBFF']
        cmaps = mcolors.ListedColormap(cwb_data,'precipitation')
        numticks = len(cwb_data) +1
        if colorlevel != colorlevelnpd and colorlevel == [0,0.1,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]:
            colorlevel = colorlevelnpd
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        elif len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [0,1,2,6,10,15,20,30,40,50,70,90,110,130,150,200,300,400]")
            colorlevel = colorlevelnpd
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    dictobj ={"levels":colorlevel,"norm":norms,"cmap":cmaps}
    return dictobj

def radar(colorlevel = [-1000, -900, 0 ,5,10,15,20,25,30,35,40,45,50,55,60,65,70], style='mosaic'):
    if style.lower() == 'cwbweb':
        cwb_data = ["#84C1FF","#2894FF","#0066CC","#28FF28","#00BB00","#009100","#F9F900","#FF8000","#FF5151","#EA0000","#AE0000","#FF44FF","#D200D2","#750075"]
        cmaps = mcolors.ListedColormap(cwb_data,'radar')
        coloraschen = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
        numticks = len(cwb_data) +1 
        if colorlevel != coloraschen and colorlevel == [-1000, -900, 0 ,5,10,15,20,25,30,35,40,45,50,55,60,65,70]:
            colorlevel = coloraschen
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        elif len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]")
            colorlevel = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    elif style.lower() == "mosaic":
        cwb_data = ["#F2F2F2","white","#07FDFD","#0695FD", "#0203F9","#00FF00","#00C800","#019500","#FEFD02","#FEC801","#FD7A00","#FB0100","#C70100","#950100","#FA03FA","#9800F6"]
        cmaps = mcolors.ListedColormap(cwb_data,'radar')
        numticks = len(cwb_data) + 1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [-1000, -900, 0 ,5,10,15,20,25,30,35,40,45,50,55,60,65,70]")
            colorlevel = [-1000, -900, 0 ,5,10,15,20,25,30,35,40,45,50,55,60,65,70]
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        #print("finish yet")
    dictobj = {"levels":colorlevel,"norm":norms,"cmap":cmaps}
    return dictobj


def surfT(colorlevel = list(range(-1,40)),style='cwbweb'):
    if style == 'cwbweb':
        cwb_data=['#117388','#207E92','#2E899C','#3D93A6','#4C9EB0','#5BA9BA','#69B4C4','#78BFCE','#87CAD8','#96D4E2','#A4DFEC','#B3EAF6','#0C924B','#1D9A51','#2FA257','#40A95E','#51B164','#62B96A','#74C170','#85C876','#96D07C','#A7D883','#B9E089','#CAE78F','#DBEF95','#F4F4C3','#F7E78A','#F4D576','#F1C362','#EEB14E','#EA9E3A','#E78C26','#E07B03','#ED5138','#ED1759','#AD053A','#780101','#9C68AD','#845194','#8520A0']
        cmaps = mcolors.ListedColormap(cwb_data,'surfT')
        numticks = len(cwb_data) +1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]")
            colorlevel = list(range(-2,41))
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    dictobj ={"norm":norms,"cmap":cmaps,"levels":colorlevel}
    return dictobj


def rh(colorlevel=[60,65,70,75,80,85,90,95,100],style="npd"):
    if style.lower() == "npd":
        cwb_data = ["None", "#D3E6EB", "#A7CFD8","#82F550","#4ADC0C","#93F4FF","#2DEAFF","#02D4E3"]
        cmaps = mcolors.ListedColormap(cwb_data,'rh')
        numticks = len(cwb_data) +1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [60,65,70,75,80,85,90,95,100]")
            colorlevel = [60,65,70,75,80,85,90,95,100]
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    if style.lower() == "rhcc":
        cwb_data = ["None", "#DAD892", "#A0E3B7", "#21F0B6", "#7ED4D8" , "#4BD6FD", "#2C928B", "#25738B" ]
        cmaps = mcolors.ListedColormap(cwb_data,'rh')
        numticks = len(cwb_data) +1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set [60,65,70,75,80,85,90,95,100]")
            colorlevel = [60,65,70,75,80,85,90,95,100]
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel, cmaps.N)
    dictobj = {"norm":norms,"cmap":cmaps,"levels":colorlevel}
    return dictobj

def freq(colorlevel = [1, 2, 5, 8, 15, 20, 25, 30, 35, 40, 100, 300, 500], plttype="hist2d", style="ccliu"):
    #Some color is took from imola colormap in the proplot package.
    defclevel = "[1, 2, 5, 8, 15, 20, 25, 30, 35, 40, 100, 300, 500]"
    if style.lower() == "ccliu":
        cwb_data = ['#2446a9', '#2d59a0', '#396b94', '#497b85', '#60927b', '#7bae74', '#99cc6d', '#c4ea67', '#ffff66', '#FFCB00', '#FF9A00', 'orangered']
        cmaps = mcolors.ListedColormap(cwb_data,'freq')
        numticks = len(cwb_data) + 1
        if len(colorlevel) != numticks:
            print("the length of colorlevel (len(colorlevel)) need {:d}.".format(numticks))
            print("Now use default set {}".format(defclevel))
            colorlevel = [1, 2, 5, 8, 15, 20, 25, 30, 35, 40, 100, 300, 500]
            norms = mcolors.BoundaryNorm(colorlevel,cmaps.N)
        else:
            norms = mcolors.BoundaryNorm(colorlevel,cmaps.N)
    if plttype == "hist2d":
        dictobj = {"norm":norms,"cmap":cmaps}
    else:
        dictobj = {"norm":norms,"cmap":cmaps,"levels":colorlevel}
    return dictobj
