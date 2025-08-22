import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as pltdate
import matplotlib.animation as animation
import seaborn as sns
import datetime as dt
import csv
from matplotlib.font_manager import fontManager, FontProperties


PALETTE = ["#97d8c4",
                     "#dd6663",
                     "#f0f2f1",
                     "#4059ad",
                     "#263568"]

def setup_theme():
    
    path = "din-condensed-bold.ttf"
    fontManager.addfont(path)
    prop = FontProperties(fname=path)
    sns.set_theme(font=prop.get_name(), palette=PALETTE, 
                  style={"text.color":"white",
                         "xtick.color":"white",
                         "ytick.color":"white",
                         "axes.edgecolor":"white",
                         "xtick.bottom":False,
                         "ytick.left":False})

# Information source:
# https://www.marketwatch.com/investing/stock/geo/download-data?startDate=8/16/2024&endDate=08/15/2025


# START_DATE = np.dot([31, 1, 365], [8, 16, 2024])

# def date_to_numdays(date_str : str):
#     return np.dot([31, 1, 365], list(map(int, date_str.split("/")))) - START_DATE

def get_data_from(filename):
    dic = []
    dates = []
    
    with open(filename) as file:
        stocks = csv.reader(file)
        next(stocks) # it has a header
        
        for day in stocks:
            # yield day[0], day[1]
            # dic[date_to_numdays(day[0])] = float(day[1])
            dates.append(dt.datetime.strptime(day[0], "%m/%d/%Y").date())
            dic.append(float(day[1]))
    dic.reverse()
    dates.reverse()
    return dates, dic

dates, datas = get_data_from("STOCK_US_XNYS_GEO.csv")
# print(datas)

# sns.set_theme()
# sns.set_style("whitegrid")
setup_theme()
fig, ax = plt.subplots()

WINDOW_SIZE = len(datas)

line, = ax.plot(dates, datas)
# ax.set_xlabel("Date")
# ax.set_ylabel("GEO Group Stock Price [$]")
# ax.set_ylabel("[$]")
ax.set_xlim(dates[0], dates[-1])

# loc = pltdate.WeekdayLocator(byweekday=pltdate.MO, interval=2)
aloc = pltdate.MonthLocator()
ax.xaxis.set_major_locator(aloc)
ax.xaxis.set_major_formatter(pltdate.DateFormatter("%m/%y"))
ax.grid(False)

ax.set_title("NYSE:GEO")

ax.text(0.05,0.9,"$",transform=ax.transAxes,fontsize=12,color=PALETTE[0])
ax.text(0.06,0.86,str(datas[0]),transform=ax.transAxes,fontsize=30,color=PALETTE[0])
ax.text(0.05,0.82,"",transform=ax.transAxes,fontsize=8,color=PALETTE[1])
ax.set_facecolor(PALETTE[-1])
fig.set_facecolor(PALETTE[-2])

def anim(i):
    i = i + 1
    data = datas[:i]
    date = dates[:i]
    
    if i >= WINDOW_SIZE:
        # if i < len(datas) - WINDOW_SIZE:
        #     ax.set_xlim(dates[i-WINDOW_SIZE], dates[i+WINDOW_SIZE])
        # else:
        #     ax.set_xlim(dates[i-WINDOW_SIZE], dates[-1])
        data = datas[i-WINDOW_SIZE:i]
        date = dates[i-WINDOW_SIZE:i]
    
    line.set_data(date, data)
    # ax.set_ylim(min(data)-5, max(data)+5)
    
    ax.texts[1].set_text(f'{data[-1]}')
    if i > 30 and i < len(datas):
        diff_lastm = datas[i] - datas[i-30]
        if diff_lastm >= 0:
            ax.texts[2].set_text(f'+{diff_lastm:2.2f} (+{100*diff_lastm/datas[i-30]:2.2f}%) past month')
            ax.texts[2].set_color(PALETTE[0])
        else:
            ax.texts[2].set_text(f'-{-diff_lastm:2.2f} (-{-100*diff_lastm/datas[i-30]:2.2f}%) past month')
            ax.texts[2].set_color(PALETTE[1])
        
    # if len(ax.texts) > 0:
    #     ax.texts[0].remove()
    # if a is not None:
    #     a.remove()
    # ax.text(date[-1], data[-1], str(data[-1]))
    
    return line,


# anim(60)
# fig.savefig("testing.png",dpi=300)
a = animation.FuncAnimation(fig, anim, blit=False, frames=len(datas), interval=100)
# a.save("stocks.gif",dpi=300, savefig_kwargs={"transparent": True})
a.save("stocks_notransparent.mp4",dpi=300)
plt.show()