import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
import seaborn as sns
import csv

def get_data_from(filename):
    dic = []
    # dictt = {}
    
    with open(filename) as file:
        areas = csv.reader(file)
        # header = next(areas) # it has no header
        
        for area in areas:
            # yield day[0], day[1]
            # dic[date_to_numdays(day[0])] = float(day[1])
            dic.append(list(map(int,area[1:-3])))
            # dictt["year"] = area[0]
        return dic#, dictt

data = get_data_from("jon_data.csv")

# return {cbp: w[1],
    #         ice: w[2],
    #         uccis: w[3],
    #         dhs: w[4],
    #         uscg: 0.25*w[5], 
    #         usss : w[6], 
    #         usms : w[7], 
    #         fbi : w[8], 
    #         dea : w[9], 
    #         atf : w[10], 
    #         traffic : w[11], 
    #         irs : w[12], 
    #         ucsp : w[13], 
    # };

# iic_arr = ["ice","cbp","uccis","dhs","uscg"]

sns.set_theme()
fig, ax = plt.subplots()

years = np.arange(2003, 2025).astype(int)

colors = ["darkblue"] * 5 + ['g','orange','r','purple','y','c','m']
labels = ["cbp", "ice", "uccis","dhs","uscg","usss",
            "usms","fbi",'dea',"atf","traffic","irs","ucsp"]

# lines = ax.stackplot(years, data[0])

def start():
    ax.stackplot(years[0], np.transpose(data[0]))

def anim(i, ax):
    ax.cla()
    ax.stackplot(years[:i], np.transpose(data[:i]), colors=colors, labels=labels)
    ax.set_xlabel("Year")
    ax.set_ylabel("Spending, [million $]")
    ax.legend(loc="upper left")
    return ax,


# anim(len(years), ax)


# fig.text()

a = animation.FuncAnimation(fig, anim, blit=False, repeat=False, frames=23, interval=200, fargs=(ax,))
# plt.show()
a.save("area_chart.gif", dpi=300,savefig_kwargs={"transparent": True})

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
