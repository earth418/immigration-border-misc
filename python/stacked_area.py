import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
import seaborn as sns
import csv
from matplotlib.font_manager import fontManager, FontProperties


def get_data_from(filename):
    dic = []
    # dictt = {}
    
    with open(filename) as file:
        areas = csv.reader(file)
        # header = next(areas) # it has no header
        
        for area in areas:
            dic.append(list(map(int,area[1:-3])))
        return dic

data = get_data_from("jon_data.csv")

years = np.arange(2003, 2025).astype(int)

colors = {
    "fbi":"#004d65",
    "dea":"#66a4b7",
    "usms":"#abe9fd",
    "atf":"#c38b57ff",
    "usss":"#9f7146ff",
    "uscg":"#dac3ad",
    "ice":"#ffb803",
    "cbp":"#fee5a0"
}

labels = ["cbp", "ice", "uccis","dhs","uscg","usss",
            "usms","fbi",'dea',"atf","traffic","irs","ucsp"]

order = ["fbi","dea","usms","atf","usss","uscg","cbp","ice"]


data_combined = [zip(labels, map(lambda x: x/1000, year)) for year in data]
data_combined = [[x for x in dc_yr if x[0] in order] for dc_yr in data_combined]
data_in_order = [sorted(dc_yr, key=(lambda x: order.index(x[0]))) for dc_yr in data_combined]

just_data = [[d for _,d in do_yr] for do_yr in data_in_order]

color_list = [colors[c] for c in order]

path = "din-condensed-bold.ttf"
fontManager.addfont(path)
prop = FontProperties(fname=path)
sns.set_theme(font=prop.get_name(), 
                style={"axes.grid":False,
                        "xtick.bottom":False,
                        "ytick.left":False})

fig, ax = plt.subplots()
fig.set_size_inches(8,4.5)
fig.subplots_adjust(left=0.15,right=0.85)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

def start():
    anim(0, ax)

def anim(i, ax):
    ax.cla()
    ax.tick_params(axis="y",pad=-4)
    ax.tick_params(axis="x",pad=-4)
    ax.set_title("Federal Law Enforcement Spending")
    ax.stackplot(years[:i], np.transpose(just_data[:i]), 
                 colors=color_list, labels=labels)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 70)
    # ax.set_ylabel("Federal spending, [billion $]")
    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)

    ax.set_yticks(range(10,70,10))
    ax.set_yticklabels([f'{a}' for a in range(10,70,10)])
    ax.set_xticks(range(years[0],years[-1]+1,3))
    
    tt = 0
    if i > 0:
        for dd in data_in_order[i-1]:
            if dd[0] == "atf" or dd[0] == "usms":
                continue
            ax.text(years[i-1], (2*tt + dd[1]) / 2, 
                    f' {dd[0].upper()}: ${dd[1]}B',
                    color=colors[dd[0]],
                    fontsize=16 if dd[0] == "ice" or dd[0] == "cbp" else 7)
            tt += dd[1]
    
    return ax,


# anim(len(years), ax)


# fig.text()

a = animation.FuncAnimation(fig, anim, init_func=start, blit=False, repeat=False, frames=23, interval=200, fargs=(ax,))
# plt.show()
# a.save("area_chart.gif", dpi=300,savefig_kwargs={"transparent": True})
a.save("area_chart.mp4", dpi=250)

# def animate(i):
#     print(i)
    
#     lines = ax.stackplot(years, np.transpose(data[:i]))
#     return (lines,np.arange(i))
    # fig.append(np.transpose(data)[i+1])
    # lines.set_array(np.transpose(data[:i+1]))
    # lines[0].
    # # linep
    # # return (line,)
    # return (lines,)

# plt.show()
# plt.show()
