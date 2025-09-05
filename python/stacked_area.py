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

# print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
# 1/0

# Adding 2025 data from Cabo Institute
# https://www.cato.org/blog/deportations-add-almost-1-trillion-costs-gops-big-beautiful-bill

# for rd in raw_data:
#     rd.append(0.0) # add bbb column

# fy_2025 = [a for a in raw_data[-1]]
# fy_2025[-1] += 167100.0
# raw_data.append(fy_2025)

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
fig.set_facecolor("#00ff00")
ax.set_facecolor("#00ff00")

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
        ax.set_title("Federal Law Enforcement Spending",color="white")
        # plt.axes().set_title()
    
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
        ax.xaxis.set_tick_params(colors="white")
        ax.yaxis.set_tick_params(colors="white")

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
                    fontsize=16 if dd[0] == "ice" or dd[0] == 'bbb' or dd[0] == "cbp" else 13)
            tt += dd[1]
    
    return ax,

a = animation.FuncAnimation(fig, anim, init_func=start, blit=False, repeat=False,
                            frames=range(0,len(data)+1), interval=80, fargs=(ax,))


a.save(("notext" if not with_text else "") + "area_chart.mp4", dpi=300)
# a.save("area_chart.gif", dpi=300,savefig_kwargs={"transparent": True})

# a.save("stacked.gif",dpi=300)
# plt.show()

def bbb():
    bbb_data = []


    # [non-immigration, immigration]
    # year1 = [0,0]

    imm = []
    non_imm = []
    for year in data_in_order:
        imm_t = non_imm_t = 0
        for x, y in year:
            if x == "ice" or x == "cbp":
                imm_t += y
            elif x == "uscg":
                imm_t += y * 0.25
            else:
                non_imm_t += y
        imm.append(imm_t)
        non_imm.append(non_imm_t)

    # immis = ["ice","cbp","uscg"]
    # imm, non_imm = []
    # non_imm = sum(filter(lambda x: x[0] in immis, data_in_order[-1]))
    # imm = sum()

    year1 = [non_imm[-1],imm[-1]]
    year2 = [non_imm[-1] + 1.1, imm[-1] + 167.1]

    # Above is ACTUAL data
    # Below is MODELED data based on the CBO waterfall model

    non_bbb_data = [
        [float(x) / 1000, float(y) / 1000] for x, y in zip(
            '21,193	21,758	22,287	22,821	23,365	23,922	24,494	25,074	25,670	26,280	26,907'.replace(",","").split('\t')[:-2],
            '35,781	36,735	37,628	38,530	39,449	40,389	41,354	42,333	43,339	44,370	45,428'.replace(",","").split('\t')[:-2]
        )]

    just_bbb_data = [
        [float(x) / 1000, float(y) / 1000] for x, y in zip("0	61	188	333	469	94	25	0	0	0".split("\t"),
        "0	6,467	10,273	15,082	18,799	13,657	8,207	2,625	-530	-1,122".replace(",","").split('\t')
    )]


    print(non_bbb_data)

    bbb_data = []
    for i in range(len(non_bbb_data)):
        bbb_data.append([
            non_bbb_data[i][0] + just_bbb_data[i][0],
            non_bbb_data[i][1] + just_bbb_data[i][1]
        ])

    # for i in range(INTERP):
    #     bbb_data.append([((ayear2 - ayear1) * i/(INTERP) + ayear1) for ayear1,ayear2 in zip(year1,year2)])
    # print(f"From {year1} to {year2}:")
    # print(bbb_data)


    data2 = [[non_imm[i], imm[i]] for i in range(0,len(data_in_order),INTERP)]
    years2 = list(np.linspace(2024, 2025, len(data2))) + list(np.linspace(2025, 2034, len(bbb_data)))
    # print()
    full_data2 = data2 + bbb_data


    # print(year1)

    # 1/-

    ax.xaxis.set_visible(False)
    if not with_text:
        ax.yaxis.set_visible(False)


        # "ice":"#ffb803ff",
        # "cbp":"#fee5a0ff",
    immi_color = "#ffd060"
    non_immi_c = "#4A9EA0"

    # T = 0

    def anim2(i, ax):
        
        i = max(0,i - 5)
        i = min(len(full_data2) - len(data2), i)
        # i =
        ax.cla()
        ax.tick_params(axis="y",pad=-4)
        # ax.tick_params(axis="x",pad=-4)
        if with_text:
            ax.set_title("Federal Law Enforcement Spending")
            
        ld2 = len(data2)
        d_index = ld2 + i
        _years = years2[:d_index]
        _data = np.transpose(full_data2[:d_index])
        
        ax.stackplot(years2[:ld2], np.transpose(data2), 
                        colors=[non_immi_c,immi_color], labels=labels)
        
        if i > 0:
            ax.vlines(2025, 0, sum(data2[-1]),color="red",linestyle="--")
            # plt.axhspan(0, 100, 0, 100, facecolor="0.2",alpha=0.5,zorder=1)
            plt.fill_between(_years[ld2:],np.zeros((i)),_data[0][ld2:],alpha=0.5,facecolor=non_immi_c)
            plt.fill_between(_years[ld2:],_data[0][ld2:],_data[0][ld2:]+_data[1][ld2:],alpha=0.5,facecolor=immi_color)

        if with_text:
            curr = full_data2[d_index-1]
            ax.text(years2[d_index-1], curr[0] / 2, 
                    f' {'OTHER'}: ${curr[0]:2.2f}B')
            ax.text(years2[d_index-1], curr[0] + (curr[1] / 2), 
                    f' {'IMMIGRATION'}: ${curr[1]:2.2f}B')
            
                    # color=colors[dd[0]],
                    # fontsize=16 if dd[0] == "ice" or dd[0] == 'bbb' or dd[0] == "cbp" else 7)
            # tt += dd[1]
        
        return ax,

    # with_text = False

    # b = animation.FuncAnimation(fig, anim2, init_func=start, fargs=(ax,), interval=200,frames=len(full_data2)-len(data2)+10)
    # b.save(("notext_" if not with_text else "") + "bbb_area_chart.mp4", dpi=300)


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
