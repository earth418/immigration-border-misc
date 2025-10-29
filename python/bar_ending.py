import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
import seaborn as sns
# import csv
from matplotlib.font_manager import fontManager, FontProperties
from pyfonts import load_google_font



Lora = load_google_font("Lora",weight="bold")
Source = load_google_font("Source Sans 3")
SourceLight = load_google_font("Source Sans 3", weight="light")

fontManager.addfont(Lora.get_file())
fontManager.addfont(Source.get_file())
fontManager.addfont(SourceLight.get_file())


sns.set_theme(font=Source.get_name(), 
                style={"axes.grid":False,
                        "xtick.bottom":False})
                        # "ytick.left":False})

# def get_data_from(filename):
#     dic = []
#     # dictt = {}
    
#     with open(filename) as file:
#         areas = csv.reader(file)
#         # header = next(areas) # it has no header
        
#         for area in areas:
#             dic.append(list(map(int,area[1:-2])))
#         return dic

# raw_data = get_data_from("jon_data.csv")

# print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
# 1/0

# Adding 2025 data from Cabo Institute
# https://www.cato.org/blog/deportations-add-almost-1-trillion-costs-gops-big-beautiful-bill


# ICE detention budget for 2024, 2025, 2026 new budget, and (projected) over  
# the following three years (BBB time period)

# From https://www.dhs.gov/sites/default/files/2025-06/25_0613_ice_fy26-congressional-budget-justificatin.pdf
# And using congressional waterfall spending
# Dollars in thousands

# x = 4e6
linear_regression = lambda x : 373903.5 * x + 3471984.17


years = list(range(2024, 2030))

detention_no_bbb = [
    3434952,
    3919952,
    4182759,
    linear_regression(3),
    linear_regression(4),
    linear_regression(5)
]

# This information comes from the American Immigration Council
# https://www.americanimmigrationcouncil.org/fact-sheet/house-reconciliation-bill-immigration-border-security/


bbb_add = [0, 0] + [10.6e6] * 4

fig, ax = plt.subplots()
fig.set_size_inches(8, 4.5)
fig.set_facecolor("green")
ax.set_facecolor("green")
fig.subplots_adjust(left=0.15,right=0.9, bottom=0.2)

# ax.set_title("ICE Detention Budget")

plt.rcParams.update({'font.size': 10})

dtn_color = "#e68c3d"
add_color = "#e23500"

def init():
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(0.25)
    ax.spines['bottom'].set_linewidth(0.25)

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    
    # ax.set_facecolor("green")
    
    ax.set_ylim(0.0, 16.5 * 1e6)
    ax.set_yticks(np.arange(4000000, 16000001, 4000000))
    ax.set_yticklabels(["$4B", "$8B","$12B","$16B"], fontsize=8, color='white')
    ax.tick_params(axis='y', color='white')
    
    ax.set_xticks(years)
    # Projected, for 2027, 28, 29
    ax.set_xticklabels(["2024", "2025", "2026", "2027*", "2028*", "2029*"], fontsize=6, color='white')
                    #    rotation=45, ha='right')
    ax.tick_params(axis='x', length=0)
    # ax.cla()

dtn_bar = ax.bar(years, 0.0, 0.8, 0.0, 
                 color=dtn_color,
                 edgecolor='white', 
                 linewidth=0.25)

hatch = '/////'
# hatch = 'xxxxx'

add_bar = ax.bar(years, 0.0, 0.8, detention_no_bbb,
                 color=dtn_color + 'aa', hatch=hatch,
                 hatch_linewidth = 0.25,
                 edgecolor='white', 
                 linewidth=0.0)

FP_YEAR = 15

NUM_FRAMES = (FP_YEAR * 2) * (len(years) + 2)

def anim(frame):
    
    # if frame < NUM_FRAMES / 2:
    
    
    for i in range(len(years)):
        
        alpha = 1 / (1 + np.exp(-4.0 * (frame / FP_YEAR - i)))
        
        # dtn_alpha = np.clip(alpha, 0.0, 0.6) / 0.6
        # add_alpha = np.clip(alpha - 0.6, 0.0, 0.4) / 0.4
        
        dtn_bar[i].set_height(detention_no_bbb[i] * alpha)
        # dtn_bar[i].set(linewidth=alpha)
        # dtn_bar[i].set_height(detention_no_bbb[i] * dtn_alpha)
        # add_bar[i].set_height(bbb_add[i] * add_alpha)
    
    # else:
    fm = 2*(frame - NUM_FRAMES/2)
    
    for i in range(2,len(years)):
        alpha = 1 / (1 + np.exp(-4.0 * (fm / FP_YEAR - i)))
        add_bar[i].set_height(bbb_add[i] * alpha)
        add_bar[i].set(linewidth=0.25*np.ceil(alpha - 0.01))




an = FuncAnimation(fig, anim, frames=NUM_FRAMES, interval=30, init_func=init)
an.save("detention_funding.mp4", dpi=240)
        # codec='png', 
        # savefig_kwargs={"transparent": True, "facecolor": "none"})

# plt.show()
