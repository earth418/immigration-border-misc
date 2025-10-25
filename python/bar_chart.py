import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.animation import FuncAnimation

def get_data_from(filename):
    dic = []
    # dictt = {}
    
    with open(filename) as file:
        areas = csv.reader(file)
        # header = next(areas) # it has no header
        
        for area in areas:
            dic.append(list(map(int,area[1:-2])))
        return dic

raw_data = get_data_from("jon_data.csv")

ice_data = [rd[1] for rd in raw_data]
cbp_data = [rd[0] for rd in raw_data]

ice_color = "#ffe3c8"
cbp_color = "#ffcf52"

years = years = np.arange(2003, 2025)

fig, ax = plt.subplots()
fig.set_size_inches(8, 4.5)
fig.set_facecolor("green")
fig.subplots_adjust(left=0.15,right=0.9, bottom=0.2)

plt.rcParams.update({'font.size': 8})

def init():
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(0.25)
    ax.spines['bottom'].set_linewidth(0.25)

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    
    ax.set_facecolor("green")
    
    ax.set_ylim(0.0, 35000)
    ax.set_yticks(np.arange(5000, 35001, 10000))
    ax.set_yticklabels(["$5B", "$15B","$25B", "$35B"], fontsize=8, color='white')
    ax.tick_params(axis='y', color='white')
    
    ax.set_xticks(years)
    ax.set_xticklabels(['2003']+ [f'\'{y % 2000:02d}' for y in years[1:]], fontsize=6, color='white')
                    #    rotation=45, ha='right')
    ax.tick_params(axis='x', length=0)
    # ax.cla()

cbp_bar = ax.bar(years, 0.0, 0.8, 0.0, 
                 color=cbp_color,)
                #  edgecolor='black', 
                #  linewidth=1)

ice_bar = ax.bar(years, 0.0, 0.8, cbp_data,
                 color=ice_color,)
                #  edgecolor='black', 
                #  linewidth=0.25)

FP_YEAR = 6

def anim(frame):
    
    for i in range(len(ice_data)):
        
        alpha = 1 / (1 + np.exp(-2.0 * (frame / FP_YEAR - i)))
        
        cbp_alpha = np.clip(alpha, 0.0, 0.6) / 0.6
        ice_alpha = np.clip(alpha - 0.6, 0.0, 0.4) / 0.4
        
        cbp_bar[i].set_height(cbp_data[i] * cbp_alpha)
        ice_bar[i].set_height(ice_data[i] * ice_alpha)
    
    # i = frame // 10
    # cbp_alpha = np.clip(frame % 10 + 1, 1, 6) / 6
    # ice_alpha = (np.clip(frame % 10 + 1, 6, 10) - 6) / 4
    
    # cbp_bar[i].set_height(cbp_data[i] * cbp_alpha)
    # ice_bar[i].set_height(ice_data[i] * ice_alpha)
    
    # if frame % 10 == 0:
    
    
    

an = FuncAnimation(fig, anim, frames=(len(ice_data) + 2) * (FP_YEAR + 1), interval=30, init_func=init)
an.save("bar_chart_funding_yearssimple.mp4", dpi=240)
        # codec='png', 
        # savefig_kwargs={"transparent": True, "facecolor": "none"})

plt.show()

# print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
