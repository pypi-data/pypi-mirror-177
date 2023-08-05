import netCDF4 as nc
import matplotlib.pyplot as plt                                                     
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.widgets import Button
from mpl_toolkits.basemap import Basemap
from wrf import  getvar, get_basemap, to_np, latlon_coords, CoordPair, vertcross
def get_layer_from_varname(var_name):
    if ("#" in var_name): 
      var_name, layer = var_name.split("#",-1)
      layer = int(layer)
      if (layer <0): 
        print("layer index less than zero")
    else:
      layer = 0
    return var_name, layer 
def  diff_index(diff,i):
     """ return boolen for difference or not """
     if(diff==-1):
        return True
     elif (diff==0):	
        return False
     else:	
        for elements in diff:
            if (elements==i+1): return True
        return False	    
    
def nc_diff(nc_f1, nc_f2,var_list, nrows=0,var_cmap=None, bm=None, diff=-1, mtitle=None, density=10):
  """
  Quick difference for two nc files for example
  nc_diff(nc_fid, nc_fid1,var_list, nrows=0,var_cmap=None)
  Aruguments:
  nc_fid1:first nc-file id,object from nc_fid=nc.Dataset("filename",'r') 
  nc_fid2:second nc-file id, same type as nc_fid
  var_list: string sequence of variable. var_list="T2 U10 V10"
  nrows: number of rows for subplot, defualt is automatic adjustment(nrows=0).
  var_cmap: string sequence of varcmap, which is same size as var_list, default is "jet". var_cmap="jet coolwarm Spectral"
  bm: Object from Basemap module. define plot area settings
  diff: index of subplots should be differnce for exmaple 3X2 subplot.ex: diff=1,2,5 
                                  |_1_|_2_|_3_|
				  |_4_|_5_|_6_|
        -1:all subplots are difference
	0 :all subplots are first file variables
  mtitle: index of main title for two files directory default("None")
          for example mtitle=(-4, -3) 
  nc_f1 = '/data2/datafdda/xa36/EX_SFCDA/CNTL/ncdf/17070603/wrfout_d01_2017-07-06_03:00:00'
                                          -4   -3    -2              -1
  nc_f2 = '/data2/datafdda/xa36/EX_SFCDA/3DVAR/SFC/17070603/wrfout_d01_2017-07-06_03:00:00'
                                               -3    -2         -1
            may print out main title " CNTL v.s. SFC "					        
  density: vectory density for wind vector plot default is 10
	

  """

  var_name = var_list.split()
  nvar = len(var_name)
  var = list()

  if (var_cmap is None):
     print("no_var_cmap")
     var_cmap = 'jet '*nvar

  var_cmap = var_cmap.split()

  ## Read NC FILE
  nc_fid1=nc.Dataset(nc_f1,'r')
  nc_fid2=nc.Dataset(nc_f2,'r')

  for i in range(nvar):
     print(var_name[i])
     var_name[i], level = get_layer_from_varname(var_name[i])
     if("." in var_name[i]):
        nfile = int(var_name[i].split(".",-1)[-1])
        if(nfile==2):
           nc_read = nc_fid2
        else:
           nc_read = nc_fid1
        var_name[i] = var_name[i].split(".",-1)[0]
     else:
       nc_read=nc_fid1
       nfile = 1
     if ("wspd" in var_name[i]):
        if ("Z" in getvar(nc_read,var_name[i]).MemoryOrder):
          print("please specify the level")
#          var.append(getvar(nc_read,var_name[i])[0][level,:,:])
          var=getvar(nc_read,var_name[i], units="m s-1")[0][level,:,:]
          data = getvar(nc_read,var_name[i], units="m s-1")[0][level,:,:].data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i], units="m s-1")[0][level,:,:].data
  
        else:
#          var.append(getvar(nc_read,var_name[i], units="m s-1")[0])
          var=(getvar(nc_read,var_name[i], units="m s-1")[0])
          data = getvar(nc_read,var_name[i], units="m s-1")[0].data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i], units="m s-1")[0].data
    
     elif ("uvmet" in var_name[i]):
        if ("Z" in getvar(nc_read,var_name[i]).MemoryOrder):
          print("please specify the level")
#          var.append(getvar(nc_read,var_name[i])[:,level,:,:])
          var=(getvar(nc_read,var_name[i])[:,level,:,:])
          data = getvar(nc_read,var_name[i])[:,level,:,:].data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i])[:,level,:,:].data
  
        else:
#          var.append(getvar(nc_read,var_name[i], units="m s-1"))
          var=(getvar(nc_read,var_name[i], units="m s-1"))
          data = getvar(nc_read,var_name[i], units="m s-1").data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i], units="m s-1").data
    
     else:
       if ("Z" in getvar(nc_read,var_name[i]).MemoryOrder):
          print("please specify the level")
#          var.append(getvar(nc_read,var_name[i])[level,:,:])
          var=(getvar(nc_read,var_name[i])[level,:,:])
          data = getvar(nc_read,var_name[i])[level,:,:].data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i])[level,:,:].data
       else:	
#          var.append(getvar(nc_read,var_name[i]))
          var=(getvar(nc_read,var_name[i]))
          data = getvar(nc_read,var_name[i]).data

          if diff_index(diff,i):
             data1 = getvar(nc_fid2,var_name[i]).data

     if diff_index(diff,i):
        val_diff = data-data1
        var.data=val_diff
     if ("wspd" in var.name): var.name=var.name.split("_",-1)[0]
     if(i==0):
       ## initialize figure
       fig = plt.figure()
       #Get the latitude and longtitude points
       lats, lons = latlon_coords(var)
       
       #Get the basemap object
       if (bm is None or type(bm)==str):
         if(bm is "Taiwan"):
             bm = get_basemap(var,resolution='i',llcrnrlon=119.0,llcrnrlat=21.8,\
                  urcrnrlon=122.05,urcrnrlat=25.4)
         else:
             bm = get_basemap(var,resolution='i')
         bm.drawcoastlines(linewidth=0.25)
         bm.drawcountries(linewidth=0.25)
         bm.drawcounties(linewidth=1.0)
       
       #Convert Lats, lons to x and y meshgrid in numpy format for plotting usage 
       x, y= bm(lons.data, lats.data)
       
       ##Create figure and subplot
       ##determine the nrows and ncols
       if (nrows ==0):
         nrows=int(np.floor(np.sqrt(nvar)))
        
       ncols=round((nvar/nrows))
       if (ncols*nrows < nvar): 
          ncols=ncols+1
       
       cob=list()
       ax=list()
       color_range={}
       nfile_dict={str(i):nfile}
       ax.append(plt.subplot(nrows,ncols,i+1))
     else:
       nfile_dict.update({str(i):nfile})
       ax.append(plt.subplot(nrows,ncols,i+1,sharex=ax[i-1],sharey=ax[i-1]))
       
     ##Add geographic outlines
     bm.drawcoastlines(ax=ax[i])
     bm.drawcountries(ax=ax[i])

     #Add filled contour and colorbar 
     density=10
     if diff_index(diff,i):
        if (len(var)==2):
           cob.append(bm.quiver(x[::density,::density], y[::density,::density], var[0][::density,::density], var[1][::density,::density], np.sqrt(var[0]**2+var[1]**2)[::density,::density],
                     scale=30, scale_units ='width', width=0.01, edgecolor='k' , linewidths=1, ax=ax[i],cmap=get_cmap(var_cmap[i]),pivot='mid', minshaft=2))
        else:		   
           cob.append(bm.contourf(x, y,var,10,cmap=get_cmap(var_cmap[i]),ax=ax[i]))

        plt.colorbar(cob[i],shrink=.32,ax=ax[i])
     else:
       if var.name in color_range:
          if (len(var)==2):
              cob.append(bm.quiver(x[::density,::density], y[::density,::density], var[0][::density,::density], var[1][::density,::density], np.sqrt(var[0]**2+var[1]**2)[::density,::density],
                   scale=60 ,scale_units ='width', width=0.01, edgecolor='k' , linewidths=1, ax=ax[i],cmap=get_cmap(var_cmap[i]),
		   clim=(min(color_range[var.name]),max(color_range[var.name])),pivot='mid', minshaft=2))
          else:
             cob.append(bm.contourf(x, y,var,color_range[var.name], cmap=get_cmap(var_cmap[i]),ax=ax[i]))
          plt.colorbar(cob[i],shrink=.32,ax=ax[i])
       else:
          if (len(var)==2):
             cob.append(bm.quiver(x[::density,::density], y[::density,::density], var[0][::density,::density], var[1][::density,::density], np.sqrt(var[0]**2+var[1]**2)[::density,::density],
                 scale=60,scale_units ='width', width=0.01, edgecolor='k' , linewidths=1, ax=ax[i],cmap=get_cmap(var_cmap[i]),pivot='mid', minshaft=2))
          else:		 
             cob.append(bm.contourf(x, y,var,10,cmap=get_cmap(var_cmap[i]),ax=ax[i]))
          cb = plt.colorbar(cob[i],shrink=.32,ax=ax[i])
          color_range.update({var.name:cb._boundaries})

  
     #Draw title   
     var.name=var.name+" eta="+str(level)
     if diff_index(diff,i):
        var.name = var.name+" difference "
     else:
        var.name = var.name+" file"+str(nfile)

     ax[i].set_title(var.name+' at \n'+str(var.Time.data).replace("T"," ")[0:-10]+" UTC")

#     print(ax[0].title._text)
#     quit()
  if (len(nc_f1.split("/",-1))==1 or len(nc_f2.split("/",-1))==1 or mtitle==None):
     plt.suptitle(nc_f1 +'\n vs. \n'+ nc_f2)
  else:   
     plt.suptitle(nc_f1.split("/",-1)[mtitle[0]] +'\n vs. \n'+ nc_f2.split("/",-1)[mtitle[1]])
  #figManager = plt.get_current_fig_manager()
  #figManager.window.showMaximized()
  sub_linebuilders = subplotsLineBuilder(ax, bm, var_name, nc_fid1, nc_fid2, nfile_dict, diff)
  
  plt.show()
  plt.tight_layout()



def vertical_plot(lat, lon ,var_name,nc_fid1, nc_fid2, nfile, diff=False):
     if (nfile==1):
       nc_fid = nc_fid1
     elif (nfile==2):  
       nc_fid = nc_fid2

     if ("wspd" in var_name):
        var =getvar(nc_fid, var_name, units="m s-1")[0]
        if (diff is True):
           var.data = getvar(nc_fid1, var_name, units="m s-1")[0].data-getvar(nc_fid2, var_name, units="m s-1")[0].data
     else:
        var =getvar(nc_fid, var_name)
        if (diff is True):
           var.data = getvar(nc_fid1, var_name).data-getvar(nc_fid2, var_name).data

     z = getvar(nc_fid, "z")
     if ("Z"not in var.MemoryOrder):  return print("cannot plot cross section")
     start_point = CoordPair(lat=lat[0], lon=lon[0])
     end_point = CoordPair(lat=lat[1], lon=lon[1])
     var_cross = vertcross(var, z, wrfin=nc_fid, start_point=start_point,
                            end_point=end_point, latlon=True, meta=True)
     #var_cross = vertcross(var, z, start_point=start_point,
     #                       end_point=end_point, latlon=True, meta=True)
     # Create the figure
     plt.figure(figsize=(12,6))
     ax = plt.axes()

     # Make the contour plot
     var_contours = ax.contourf(var_cross, cmap=get_cmap("jet"))
     

     # Add the color bar
     plt.colorbar(var_contours, ax=ax)
     
     # Set the x-ticks to use latitude and longitude labels.
     #coord_pairs = to_np(var_cross.coords["xy_loc"])
     coord_pairs = var_cross.coords["xy_loc"].data
     x_ticks = np.arange(coord_pairs.shape[0])
     x_labels = [pair.latlon_str(fmt="{:.2f}, {:.2f}")
                 for pair in to_np(coord_pairs)]
               #  for pair in coord_pairs]
     ax.set_xticks(x_ticks[::20])
     ax.set_xticklabels(x_labels[::20], rotation=45, fontsize=8)
     
     # Set the y-ticks to be height.
     vert_vals = (var_cross.coords["vertical"].data)
     v_ticks = np.arange(vert_vals.shape[0])
     ax.set_yticks(v_ticks[::10])
     ax.set_yticklabels(vert_vals[::10], fontsize=8)
     
     # Set the x-axis and  y-axis labels
     ax.set_xlabel("Latitude, Longitude", fontsize=12)
     ax.set_ylabel("Height (m)", fontsize=12)
     
     plt.title("Vertical Cross Section of "+var_name)
     
     plt.show()

     return


class LineBuilder:

    def __init__(self, ax, bm, var_name, nc_fid1, nc_fid2, ncfile_num, index, diff):
        
        self.ax = ax
        self.bm = bm
        self.var_name = var_name
        self.nc_fid1 = nc_fid1
        self.nc_fid2 = nc_fid2
        self.ncfile_num = ncfile_num
        self.index = index
        self.diff = diff

        line, = ax.plot([float('nan')], [float('nan')])  # empty line
        self.line = line

        marker, =ax.plot([float('nan')], [float('nan')], marker="o")  # empty marker
        self.markers = marker


        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

        self.xs = []

        self.ys = []

    def __call__(self, event):

        if event.inaxes!=self.line.axes: return
        if (event.button==3):
          self.xs = []
          self.ys = []
          self.line.set_data(self.xs, self.ys)
          self.markers.set_data(self.xs, self.ys)

          self.line.figure.canvas.draw()

          return
        if (event.dblclick is True):
          self.xs.append(event.xdata)
          self.ys.append(event.ydata)
          self.markers.set_data(self.xs, self.ys)
          self.line.set_data(self.xs, self.ys)

          self.markers.set_color('k')

          self.line.figure.canvas.draw()
        if (len(self.xs)>=2 and event.button==2):
           print("plotting")
           lon, lat = self.bm(self.xs[-2:], self.ys[-2:], inverse=True)
           vertical_plot(lat, lon , self.var_name, self.nc_fid1, self.nc_fid2,self.ncfile_num,diff=self.diff)
           return

def subplotsLineBuilder(axes, bm, var_name, nc_fid1, nc_fid2, ncfile_dict, diff):
    sub_obj=list()
    i=0
    for ax in axes:
      sub_obj.append(LineBuilder(ax, bm, var_name[i], nc_fid1, nc_fid2, ncfile_dict[str(i)],i,diff_index(diff,i)))
      i=i+1
      
    return sub_obj 


   
