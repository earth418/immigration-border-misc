import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as pltdate
import matplotlib.animation as animation
import seaborn as sns
import datetime as dt
import csv

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
print(datas)

sns.set_theme()
sns.set_style("whitegrid")
fig, ax = plt.subplots()

WINDOW_SIZE = 50

line, = ax.plot(dates, datas)
ax.set_xlabel("Date")
ax.set_ylabel("GEO Group Stock Price [$]")
ax.set_xlim(dates[0], dates[WINDOW_SIZE*2])

# loc = pltdate.WeekdayLocator(byweekday=pltdate.MO, interval=2)
aloc = pltdate.MonthLocator()
ax.xaxis.set_major_locator(aloc)
ax.xaxis.set_major_formatter(pltdate.AutoDateFormatter(aloc))
# ax.xaxis.set_minor_locator(pltdate.AutoDateLocator())

def anim(i):
    i = i + 1
    data = datas[:i]
    date = dates[:i]
    
    if i >= WINDOW_SIZE:
        if i < len(datas) - WINDOW_SIZE:
            ax.set_xlim(dates[i-WINDOW_SIZE], dates[i+WINDOW_SIZE])
        else:
            ax.set_xlim(dates[i-WINDOW_SIZE], dates[-1])
        data = datas[i-WINDOW_SIZE:i]
        date = dates[i-WINDOW_SIZE:i]
    
    line.set_data(date, data)
    ax.set_ylim(min(data)-5, max(data)+5)
        
    return line,


a = animation.FuncAnimation(fig, anim, blit=False, frames=len(datas)+1, interval=100)
a.save("stocks.gif",dpi=300, savefig_kwargs={"transparent": True})
# plt.show()