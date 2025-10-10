import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
import seaborn as sns
import csv
from matplotlib.font_manager import fontManager, FontProperties
from pyfonts import load_google_font

# path = "din-condensed-bold.ttf"
# fontManager.addfont(path)
# prop = FontProperties(fname=path)
Lora = load_google_font("Lora",weight="bold")
Source = load_google_font("Source Sans 3")
SourceLight = load_google_font("Source Sans 3", weight="light")

fontManager.addfont(Lora.get_file())
fontManager.addfont(Source.get_file())
fontManager.addfont(SourceLight.get_file())


sns.set_theme(font=Lora.get_name(), 
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

# print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
# 1/0

# Adding 2025 data from Cabo Institute
# https://www.cato.org/blog/deportations-add-almost-1-trillion-costs-gops-big-beautiful-bill


INTERP = 10

data = []
for ind,year in enumerate(raw_data[:-1]):
    if ind < len(raw_data) - 1:
        year2 = raw_data[ind+1]
        for i in range(INTERP):
            data.append([((ayear2 - ayear1) * i/INTERP + ayear1) for ayear1,ayear2 in zip(year,year2)])

data.append(raw_data[-1])


# bbb_data = 167100.0


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
    # "bbb":"#dfa7c077"
}

# print(data)
labels = ["cbp", "ice", "uccis","dhs","uscg","usss",
            "usms","fbi",'dea',"atf","traffic","irs","ucsp"]

# print(data[-1])
# print(zip(data[-1],labels))
# 1/0

order = ["fbi","dea","usms","atf","usss","uscg","cbp","ice"]


data_combined = [zip(labels, map(lambda x: x/1000, year)) for year in data]
data_combined = [[x for x in dc_yr if x[0] in order] for dc_yr in data_combined]
data_in_order = [sorted(dc_yr, key=(lambda x: order.index(x[0]))) for dc_yr in data_combined]

# print(data_in_order)
just_data = [[d for _,d in do_yr] for do_yr in data_in_order]

color_list = [colors[c] for c in order]

fig, ax = plt.subplots()
fig.set_size_inches(8,4.5)
fig.subplots_adjust(left=0.15,right=0.85)
# fig.set_facecolor("#3354b9")


with_text = False

if not with_text:
    fig.set_facecolor("#00ff00")
    ax.set_facecolor("#00ff00")

textcolor = "black"
if not with_text:
    textcolor = "white"

edgecolor = "black"
if not with_text:
    edgecolor = "white"
    

# if with_text:
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set(linewidth=0.5)
ax.spines['bottom'].set(linewidth=0.5)

ax.spines['bottom'].set_color(edgecolor)
ax.spines['left'].set_color(edgecolor) 

if not with_text:
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

def start():
    anim(0, ax)

# print(years)
# moving_texts = []

xlabels = []
ylabels = []
 
if with_text:
    yv = range(10, 70, 10)
    for i, d in enumerate(yv):
        ylabels.append(fig.text(0.12, 0.21 + 0.55 * i / (len(yv) - 1), d, font=SourceLight, color=textcolor, fontsize=10))
        # ylabels.append(fig.text(years[0], d, d, font=SourceLight, color="black", fontsize=10))
        
    yrs = range(int(years[0]),int(years[-1])+1,3)
    for i, d in enumerate(yrs):
        xlabels.append(fig.text(0.17 + 0.61 * i / (len(yrs) - 1), 0.07, str(d), font=SourceLight, color=textcolor, fontsize=10))


def anim(i, ax):
    ax.cla()
    # i = i + len(data) - 10
    # ax.tick_params(axis="y",pad=-4)
    # ax.tick_params(axis="x",pad=-4)
    if with_text:
        ax.set_title("Federal Law Enforcement Spending",color=textcolor,font=Source)
        # plt.axes().set_title()
    
    ax.stackplot(years[:i], np.transpose(just_data[:i]), 
                #  linewidth=0.33 if i < len(data) else 0.0,
                #  edgecolor='black',
                #  linestyle='solid',
                 colors=color_list, labels=labels)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 70)
    
    tot = np.zeros(i)
    for dd in np.transpose(just_data[:i]):
        tot += dd
        ax.plot(years[:i], tot, linewidth=0.5, color=edgecolor)
    
    
    # if with_text:
    #     ax.xaxis.set_tick_params(labelsize=7)
    #     ax.yaxis.set_tick_params(labelsize=7)
    #     ax.xaxis.set_tick_params(colors="white")
    #     ax.yaxis.set_tick_params(colors="white")

    #     ax.set_yticks(range(10,70,10))
    #     ax.set_yticklabels([f'{a}' for a in range(10,70,10)])
    #     ax.set_xticks(range(int(years[0]),int(years[-1])+1,3))
    ax.set_yticks([])
    ax.set_xticks([])
    
    tt = 0
    # i <= len(data)
    if i > 0 and with_text:
        for dd in data_in_order[i-1]:
            if dd[0] == "atf" or dd[0] == "usms" or dd[1] == 0:
                tt += dd[1]
                continue
            ax.text(years[i-1], (2*tt + dd[1]) / 2, 
                    f' {dd[0].upper()}: ${dd[1]:2.2f}B',
                    color=colors[dd[0]],
                    font=Lora,
                    fontsize=12 if dd[0] == "ice" or dd[0] == 'bbb' or dd[0] == "cbp" else 9)
            tt += dd[1]
    
    return ax,

a = animation.FuncAnimation(fig, anim, init_func=start, blit=False, repeat=False,
                            frames=range(0,len(data)+1), interval=80, fargs=(ax,))


a.save(("notext_" if not with_text else "") + "area_chart.mp4", dpi=300)
# plt.show()
# a.save("area_chart.gif", dpi=300,savefig_kwargs={"transparent": True})


for y in ylabels:
    y.remove()
for x in xlabels:
    x.remove()


# a.save("stacked.gif",dpi=300)

def bbb2():
  
  
    imm = []
    non_imm = []
    for year in data_in_order:
        imm_t = non_imm_t = 0
        for x, y in year:
            if x == "ice" or x == "cbp":
                imm_t += y
            elif x == "uscg":
                imm_t += y * 0.25
                non_imm_t += y * 0.75
            else:
                non_imm_t += y
        imm.append(imm_t)
        non_imm.append(non_imm_t)

    ax.set_xticks([])
    ax.set_yticks([])
    immi_color = "#ffd060"
    non_immi_c = "#4A9EA0"

    year1 = [non_imm[-1],imm[-1]]
    year2 = [non_imm[-1] + 1.1, imm[-1] + 167.1]
    
    data2 = [[non_imm[i], imm[i]] for i in range(0,len(data_in_order),INTERP)]
    years2 = list(np.linspace(2003, 2026, len(data2))) #+ [2026]
    # print()
    full_data2 = data2
    ax.set_xlim(years2[0], years2[-1] + 3)
    ax.set_ylim(0, 230.0)

    if not with_text:
        fig.set_facecolor("#00ff00")
        ax.set_facecolor("#00ff00")
    
    ax.spines['bottom'].set_color(edgecolor)
    ax.spines['left'].set_color(edgecolor) 
    
    # fig.text(0.785, 0.0475, "2025+\nBBB", font=SourceLight, horizontalalignment="center",color=textcolor)
    
    # for xlabel in xlabels:
    #     xlabel.set_color(textcolor)
    #     xlabel.set_x(0.88 * (xlabel.get_position()[0] - 0.17) + 0.17)
        # xlabel.set_x(2021, transform=ax.get_xaxis_transform())
    
    # for ylabel in ylabels:
    #     ylabel.set_y(0.32 * (ylabel.get_position()[1] - 0.21) + 0.1)
        
    
    # if with_text:
    #     # curr = year2[-1]
    #     ax.text(years2[-1]+1.75, year2[0] / 2, 
    #             f' {'OTHER'}: ${year2[0]:2.2f}B')
    #     ax.text(years2[-1]+1.75, year2[0] + (year2[1] / 2), 
    #             f' {'IMMIG.'}: ${year2[1]:2.2f}B')
    # origs = [ylabel.get_position()[1] for ylabel in ylabels]
    # new_range = ()
    
    def anim2(i, ax):
 
        ax.cla()
        
        ax.set_xticks([])
        ax.set_yticks([])
 
        
        # print(i)
        
        SCALE = 0.18
        
        if i < 20:
            
            alph = i / 20
            
            # ax.stackplot(years[:i], np.transpose(just_data[:i]), 
            ax.stackplot(years, np.transpose(just_data), 
                 linewidth=0.5,
                 edgecolor=edgecolor,
                 colors=color_list, labels=labels, alpha=(1.0 - alph))
            ax.set_xlim(years[0], years[0] + (years[-1] - years[0]) * (1 + SCALE * alph))
            # print(years[-1] * (1 + 0.15 * alph))
            ax.set_ylim(0, 70 * (1 + SCALE * alph))
            
            # new_range = range(10, 70, 15)
            # for g in new_range:
            #     ax.text(years2[0]-1.0, g, g, font=SourceLight,color=textcolor, fontsize=10)


            ax.stackplot(years2, np.transpose(data2), 
                        colors=[non_immi_c,immi_color],
                        linewidth=0.5,
                        edgecolor=edgecolor,
                        alpha = alph)
            return
        
        i = max(0,i - 30)
        i = min(40, i)
        
        if with_text:
            ax.set_title("Federal Law Enforcement Spending",color=textcolor, font=Source)

        
        alpha = i / 40
        
        ax.stackplot(years2, np.transpose(data2), 
                     colors=[non_immi_c,immi_color],
                     linewidth=0.5,
                     edgecolor=edgecolor)

        ax.set_xlim(years2[0], years[0] + (years[-1] - years[0]) * (1 + SCALE) )#* alpha)
        ax.set_ylim(0, 70 * (1 + SCALE) + 160.0 * alpha)

        # blendedTransform = ax.get_yaxis_transform() + ax.transData

        for g in range(2003, 2025, 3):
            ax.text(g, -0.05, g, font=SourceLight,color=textcolor, fontsize=10, transform=ax.get_xaxis_transform())
        ax.text(years2[-1]+1.5, -0.09, "2025+\nBBB", font=SourceLight, 
                horizontalalignment="center",color=textcolor,
                fontsize=10,transform=ax.get_xaxis_transform())


        new_range = range(10, int(70 * (1 + SCALE) + 160.0 * alpha), int(15 + 15 * alpha))
        for g in new_range:
            ax.text(years2[0]-1.0, g, g, font=SourceLight,color=textcolor, 
                    fontsize=10,horizontalalignment="center")
        
        
        
        curr = [year1[0] + (year2[0] - year1[0]) * alpha, 
                year1[1] + (year2[1] - year1[1]) * alpha]
        
        if i > 0:
            ax.bar(years2[-1] + 1.5, curr[0]*min(alpha*4,1), 1.5, 0.0, color=non_immi_c, edgecolor=edgecolor, linewidth=0.5)
            if i >= 11:
                ax.bar(years2[-1] + 1.5, curr[1]*(4/3)*max(alpha-0.25,0), 1.5, curr[0], color=immi_color, edgecolor=edgecolor, linewidth=0.5)
    
        if with_text and i == 0 or i == 40:
            ax.text(years2[-1] + 2.5*alpha, curr[0] / 2, 
                    f' {'OTHER'}: ${curr[0]:2.2f}B',
                    horizontalalignment='left',fontsize=12,color=textcolor)
            ax.text(years2[-1] + 2.5*alpha, curr[0] + (curr[1] / 2), 
                    f' {'IMMIGRATION'}:\n ${curr[1]:2.2f}B',
                    horizontalalignment='left', fontsize=10,color=textcolor)
        
        return ax,
    
    b = animation.FuncAnimation(fig, anim2, init_func=start, fargs=(ax,), interval=100,frames=80)
    # (a + b).save("stacked_area_combined.mp4",dpi=300)
    b.save(("notext_" if not with_text else "") + "bbb_area_chart.mp4", dpi=300)
    
    # plt.show()

    
bbb2()
