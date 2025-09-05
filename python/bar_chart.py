import matplotlib.pyplot as plt
import numpy as np
import csv

# import matplotlib.animation as animation
# import seaborn as sns
# from matplotlib.font_manager import fontManager, FontProperties

# path = "din-condensed-bold.ttf"
# fontManager.addfont(path)
# prop = FontProperties(fname=path)
# sns.set_theme(font=prop.get_name(), 
#                 style={"axes.grid":False,
#                         "xtick.bottom":False,
#                         "ytick.left":False})

def get_data_from(filename):
    dic = []
    # dictt = {}
    
    with open(filename) as file:
        areas = csv.reader(file)
        # header = next(areas) # it has no header
        
        for area in areas:
            dic.append(list(map(int,area[1:-2])))
        return dic

raw_data = get_data_from("python/jon_data.csv")

print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
