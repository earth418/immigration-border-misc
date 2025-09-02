import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
import seaborn as sns
import csv
from matplotlib.font_manager import fontManager, FontProperties

path = "din-condensed-bold.ttf"
fontManager.addfont(path)
prop = FontProperties(fname=path)
sns.set_theme(font=prop.get_name(), 
                style={"axes.grid":False,
                        "xtick.bottom":False,
                        "ytick.left":False})

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

# Adding 2025 data from Cabo Institute
# https://www.cato.org/blog/deportations-add-almost-1-trillion-costs-gops-big-beautiful-bill

for rd in raw_data:
    rd.append(0.0) # add bbb column

fy_2025 = [a for a in raw_data[-1]]
fy_2025[-1] += 167100.0
raw_data.append(fy_2025)

INTERP = 10

data = []
for ind,year in enumerate(raw_data[:-1]):
    if ind < len(raw_data) - 1:
        year2 = raw_data[ind+1]
        for i in range(INTERP):
            data.append([((ayear2 - ayear1) * i/INTERP + ayear1) for ayear1,ayear2 in zip(year,year2)])

data.append(raw_data[-1])

# print(data)
# 1/0
# print(data)
years = np.linspace(2003, 2026, len(data))
# print("Years:", years)

colors = {
    "fbi":"#004d65ff",
    "dea":"#66a4b7ff",
    "usms":"#abe9fdff",
    "atf":"#c38b57ff",
    "usss":"#9f7146ff",
    "uscg":"#dac3adff",
    "ice":"#ffb803ff",
    "cbp":"#fee5a0ff",
    "bbb":"#dfa7c077"
}

# print(data)
labels = ["cbp", "ice", "uccis","dhs","uscg","usss",
            "usms","fbi",'dea',"atf","traffic","irs","ucsp","bbb"]

# print(data[-1])
# print(zip(data[-1],labels))
# 1/0

order = ["fbi","dea","usms","atf","usss","uscg","cbp","ice","bbb"]


data_combined = [zip(labels, map(lambda x: x/1000, year)) for year in data]
data_combined = [[x for x in dc_yr if x[0] in order] for dc_yr in data_combined]
data_in_order = [sorted(dc_yr, key=(lambda x: order.index(x[0]))) for dc_yr in data_combined]

# print(data_in_order)
just_data = [[d for _,d in do_yr] for do_yr in data_in_order]

color_list = [colors[c] for c in order]

fig, ax = plt.subplots()
fig.set_size_inches(8,4.5)
fig.subplots_adjust(left=0.15,right=0.85)

with_text = True

# if with_text:
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

if not with_text:
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

def start():
    anim(0, ax)

# print(years)

def anim(i, ax):
    ax.cla()
    ax.tick_params(axis="y",pad=-4)
    ax.tick_params(axis="x",pad=-4)
    if with_text:
        ax.set_title("Federal Law Enforcement Spending")
    
    ax.stackplot(years[:i], np.transpose(just_data[:i]), 
                #  linewidth=1,
                #  edgecolor='black',
                #  linestyle=['solid']*(len(just_data[0])+1)
                #           +["--"],
                 colors=color_list, labels=labels)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, max(70,max(0,i-210)*25))
   
    if with_text:
        ax.xaxis.set_tick_params(labelsize=7)
        ax.yaxis.set_tick_params(labelsize=7)

        ax.set_yticks(range(10,70,10))
        ax.set_yticklabels([f'{a}' for a in range(10,70,10)])
        ax.set_xticks(range(int(years[0]),int(years[-1])+1,3))
    
    tt = 0
    
    if i > 0 and with_text:
        for dd in data_in_order[i-1]:
            if dd[0] == "atf" or dd[0] == "usms" or dd[1] == 0:
                tt += dd[1]
                continue
            ax.text(years[i-1], (2*tt + dd[1]) / 2, 
                    f' {dd[0].upper()}: ${dd[1]:2.2f}B',
                    color=colors[dd[0]],
                    fontsize=16 if dd[0] == "ice" or dd[0] == 'bbb' or dd[0] == "cbp" else 7)
            tt += dd[1]
    
    return ax,


# anim(len(years), ax)


# fig.text()

a = animation.FuncAnimation(fig, anim, init_func=start, blit=False, repeat=False,
                            frames=range(0,len(data)+1), interval=80, fargs=(ax,))
plt.show()
# a.save("area_chart.gif", dpi=300,savefig_kwargs={"transparent": True})
# a.save(("notext" if not with_text else "") + "area_chart.mp4", dpi=300)

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
