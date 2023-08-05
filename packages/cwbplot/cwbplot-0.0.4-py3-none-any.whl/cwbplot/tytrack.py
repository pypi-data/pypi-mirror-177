from matplotlib.lines import Line2D

def filled(maxws, marker='o', linestyle ='-', sizes=5):
    if maxws <= 62/3.6 and maxws >= 41/3.6:
        #markdict = dict(marker=marker, s=sizes, c='dodgerblue', edgecolors='darkblue',alpha=0.9)
        linedict = dict(linestyle=linestyle, marker=marker, markersize=sizes, markeredgecolor='darkblue',markerfacecolor='dodgerblue',color='darkblue', alpha=0.90)
    elif maxws > 41/3.6 and maxws <= 32.6:
        #markdict = dict(marker=marker, s=sizes, c='coral', edgecolors='#E35200', alpha=0.9)
        linedict = dict(linestyle=linestyle, marker=marker,  markersize=sizes, markeredgecolor='#E35200',markerfacecolor='coral',color='#E35200', alpha=0.90)
    elif maxws > 32.6 and maxws <= 50.9:
        #markdict = dict(marker=marker, s=sizes, c='indianred', edgecolors='maroon', alpha=0.9)
        linedict = dict(linestyle=linestyle, marker=marker,  markersize=sizes, markeredgecolor='maroon',markerfacecolor='indianred',color='maroon', alpha=0.90)
    elif maxws > 50.9:
        #markdict = dict(marker=marker, s=sizes, c='orchid', edgecolors='purple', alpha=0.9)
        linedict = dict(linestyle=linestyle, marker=marker, markersize=sizes , markeredgecolor='purple',markerfacecolor='orchid',color='purple', alpha=0.90)
    else:
        #markdict = dict(marker=marker, s=sizes, c='white',edgecolors='dimgray', alpha=0.9)
        linedict = dict(linestyle=linestyle, marker=marker, markersize=sizes , markeredgecolor='dimgray',markerfacecolor='white',color='dimgray', alpha=0.90)
    nontroplin2d = Line2D([0],[0], linestyle=linestyle, color = "dimgray", marker=marker,markersize=5, markeredgecolor='dimgray' , markerfacecolor='white', alpha=0.9)
    td2d = Line2D([0],[0], linestyle = linestyle, color = "darkblue", marker=marker, markersize=5, markeredgecolor='darkblue' , markerfacecolor='dodgerblue', alpha=0.9)
    mild2d = Line2D([0],[0], linestyle = linestyle, color = "#E35200", marker=marker, markersize=5, markeredgecolor='#E35200' , markerfacecolor='coral', alpha=0.9)
    mode2d = Line2D([0],[0], linestyle = linestyle, color = "maroon", marker=marker, markersize=5, markeredgecolor='maroon' , markerfacecolor='indianred', alpha=0.9)
    ser2d = Line2D([0],[0], linestyle = linestyle, color = "purple", marker=marker, markersize=5, markeredgecolor='purple' , markerfacecolor='orchid', alpha=0.9)
    handle_elements = [nontroplin2d, td2d, mild2d, mode2d, ser2d]
    lable_elements = ["Non-Tropical","TD","Mild","Moderate","Severe"]
    legend_elements = [handle_elements, lable_elements]
    return linedict, legend_elements

