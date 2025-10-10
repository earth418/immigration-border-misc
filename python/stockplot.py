import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as pltdate
import matplotlib.animation as animation
from matplotlib.ticker import MultipleLocator
import seaborn as sns
import datetime as dt
import csv

from matplotlib.font_manager import fontManager, FontProperties
from pyfonts import load_google_font

PALETTE = ["#97d8c4",
                     "#dd6663",
                     "#f0f2f1",
                     "#4059ad",
                     "#171f3a"]


# path = "din-condensed-bold.ttf"
# lora_path = "./fonts/Lora-VariableFont_wght.ttf"
# source_path = "./fonts/source-sans-3-v19-latin-regular.woff2"
# source_light = "./fonts/source-sans-3-v19-latin-300.woff2"

# fontManager.addfont(lora_path)
# Lora = FontProperties(fname=lora_path)
# # Lora.set_weight('light')

# fontManager.addfont(source_light)
# SourceLight = FontProperties(fname=source_light)
# # SourceLight.set_weight("light")

# fontManager.addfont(source_path)
# Source = FontProperties(fname=source_path)
# Source.set_weight("bold")

Lora = load_google_font("Lora")
Source = load_google_font("Source Sans 3")
SourceLight = load_google_font("Source Sans 3", weight=200)
SourceHeavy = load_google_font("Source Sans 3", weight='semi-bold')
SourceVHeavy = load_google_font("Source Sans 3", weight='black')

fontManager.addfont(Lora.get_file())
fontManager.addfont(Source.get_file())
fontManager.addfont(SourceLight.get_file())
fontManager.addfont(SourceHeavy.get_file())
fontManager.addfont(SourceVHeavy.get_file())

def setup_theme():
    
    # LoraLight = FontProperties(fname=lora_path)
    # LoraLight.set_weight("light")
    
    # prop = FontProperties(fname=lora_path)
    sns.set_theme(palette=PALETTE, 
                  font=Lora.get_name(),
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
            date = dt.datetime.strptime(day[0], "%m/%d/%Y").date()
            # if date < dt.datetime(2025, 3, 15).date():
            dates.append(date)
            dic.append(float(day[1]))
    dic.reverse()
    dates.reverse()
    return dates, dic

def plot_stock_filename(stock_name, filename,withtext):
    dates, datas = get_data_from(filename)
    # print(datas)

    # sns.set_theme()
    # sns.set_style("whitegrid")
    setup_theme()
    fig, ax = plt.subplots()
    fig.set_size_inches(8,4.5)
    fig.subplots_adjust(left=3/16, right=13/16, top=15/18, bottom=3/18)

    WINDOW_SIZE = 30

    # img = plt.imread("grid.png")
    # ax.imshow(img,vmin=0, vmax=2250) #, extent=[0, 365, 10.0, 40.0])


    # line_color = PALETTE[0] if withtext else "#ffffff"
    line_color = "#ffffff"
    # LINE IS HERE
    line, = ax.plot(dates, datas, color=line_color, linewidth=1)
    
    
    
    # ax.set_xlabel("Date")
    # ax.set_ylabel("GEO Group Stock Price [$]")
    # ax.set_ylabel("[$]")
    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(10.0, 40.0)
    
    # plt.rcParams["font"]

    # loc = pltdate.WeekdayLocator(byweekday=pltdate.MO, interval=2)
    ax.grid(False)
    # aloc = pltdate.MonthLocator(interval=2)
    # ax.xaxis.set_major_locator(aloc)
    # ax.xaxis.set_major_formatter(pltdate.DateFormatter("%m/%y"))
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    
    if withtext:
        sdates = ["9/24","11/24","01/25","03/25","05/25","07/25"]
        for d in sdates:
            ax.text(dt.datetime.strptime(d,"%m/%y"), -0.05, d,
                     font=SourceHeavy, color='black', transform=ax.get_xaxis_transform())
                    
            # fig.text(0.22 + 0.64 * i / (len(sdates) - 1), 0.07, d, 
            #          font=SourceHeavy, color='black')
            
        vals = np.arange(15, 40, 5)
        for i, val in enumerate(vals):
            ax.text(-0.04, val, str(val), font=SourceHeavy, color='black', transform=ax.get_yaxis_transform())
            
            # fig.text(0.09, 0.23 + 0.51 * i / (len(vals) - 1), str(val), 
            #          font=SourceHeavy, color='black')
      
    # minorLocatorX = MultipleLocator(1) # every day -- 365/thing
    # minorLocatorY = MultipleLocator(30 / len(dates))
    # # minorLocator = MaxNLocator(100)
    # ax.xaxis.set_minor_locator(minorLocatorX)
    # ax.yaxis.set_minor_locator(minorLocatorY)
    
    
    # 'GRID LINES GENERATE HERE'
    # if withtext:
    #     for i in np.linspace(10.0, 40.0, 30):
    #         ax.axhline(i, linewidth=0.1, color="#aaaaaa7a")

    #     for i in np.linspace(dates[0], dates[-1], int(30*16/9)):
    #         ax.axvline(i, linewidth=0.1, color="#aaaaaa7a")
        
    
    # plt.rc('text', usetex=True)
    # plt.rc('axes', linewidth=2)
    # plt.rc('font', weight='light')
    
    ax.xaxis.set_tick_params(labelfontfamily=Source.get_name(), labelcolor="#ffffffaa")
    ax.yaxis.set_tick_params(labelfontfamily=Source.get_name(), labelcolor="#ffffffaa")
    # ax.xaxis.set_fontname(SourceLight.get_name())
    
    if not withtext:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    else:
        [ax.spines[spax].set(color="black", linewidth=1) for spax in ax.spines]
    
    ax.xaxis.set_visible(withtext)
    ax.yaxis.set_visible(withtext)

    
    
    # ax.yaxis.set_visible(False)
    
    green = not withtext
    
    if green or True:
        fig.set_facecolor("#00ff00")
        ax.set_facecolor("#00ff00")
    else:
        # fig.set_facecolor(PALETTE[3])
        # ax.set_facecolor(PALETTE[4])
        # fig.set_facecolor("#776F6F")
        # fig.set_im
        
        image = plt.imread("base_resized.png")
        background_ax = plt.axes([0,0,1,1])
        background_ax.set_zorder(-2)
        # background_ax.patch.set_alpha(0.6)
        background_ax.imshow(image, aspect='auto')
        
        background_ax2 = plt.axes([0,0,1,1])
        background_ax2.set_zorder(-1)
        background_ax2.set_facecolor("#ffffff")
        background_ax2.patch.set_alpha(0.75)
        
        ax.set_facecolor("#B3A4A4")
        ax.patch.set_alpha(0.5)
        # plt.
        # background_ax.axh
        
        # for i in np.linspace(0.0, 1079.0, 36):
        for i in np.arange(0, 1080, 30):
            background_ax.axhline(i, linewidth=0.5, color="#aaaaaa7a")

        # for i in np.linspace(0.0, 1919.0, 64):
        for i in np.arange(0, 1920, 30):
            background_ax.axvline(i, linewidth=0.5, color="#aaaaaa7a")

    if withtext:
        # Source.set_weight('medium')
        ax.set_title(stock_name, fontproperties=Source, fontsize=24,fontweight="bold",color='black')

    if withtext:
        # colors = [PALETTE[0], PALETTE[0], PALETTE[1]]
        colors = ['black', 'black']
        ax.text(0.04,0.825,"$",transform=ax.transAxes,fontsize=16,color=colors[0])
        amt = ax.text(0.06,0.805,str(datas[0]),transform=ax.transAxes,fontsize=30,color=colors[0])
        chg = ax.text(0.05,0.75,"",transform=ax.transAxes,fontsize=8,color=colors[1])
        # ax.set_facecolor(PALETTE[-1])
        # fig.set_facecolor(PALETTE[-2])

    def anim(i):
        i = i + 1
        data = datas[:i]
        date = dates[:i]
        
        # if i >= WINDOW_SIZE:
        #     if i < len(datas) - WINDOW_SIZE:
        #         ax.set_xlim(dates[i-WINDOW_SIZE], dates[i+WINDOW_SIZE])
        #     else:
        #         ax.set_xlim(dates[i-WINDOW_SIZE], dates[-1])
        #     data = datas[i-WINDOW_SIZE:i]
        #     date = dates[i-WINDOW_SIZE:i]
        
        line.set_data(date, data)
        # ax.set_ylim(min(data)-5, max(data)+5)
        
        tcolors = ["#FFFFFF","#000000"]
        
        if withtext:
            amt.set_text(f'{data[-1]}')
            if i > 30 and i < len(datas):
                diff_lastm = datas[i] - datas[i-30]
                if diff_lastm >= 0:
                    chg.set_text(f'+{diff_lastm:2.2f} (+{100*diff_lastm/(datas[i-30]):2.2f}%) past month')
                    chg.set_color(tcolors[0])
                else:
                    chg.set_text(f'-{-diff_lastm:2.2f} (-{-100*diff_lastm/(datas[i-30]):2.2f}%) past month')
                    chg.set_color(tcolors[1])
            
        # if len(ax.texts) > 0:
        #     ax.texts[0].remove()
        # if a is not None:
        #     a.remove()
        # ax.text(date[-1], data[-1], str(data[-1]))
        
        return line,

    # a.save("stocks.gif",dpi=300) #, savefig_kwargs={"transparent": True})

    # anim(60)
    # fig.savefig("testing.png",dpi=300)
    a = animation.FuncAnimation(fig, anim, blit=False, frames=len(datas), interval=100)
    a.save(("notext_" if not withtext else "green_") + stock_name.split(":")[-1] + "_stocksplot.mp4",dpi=300)
    # print("Done with " + stock_name)
    # plt.show()
    
plot_stock_filename("NYSE:GEO","STOCK_US_XNYS_GEO.csv",True)
plot_stock_filename("NYSE:CXW","STOCK_US_XNYS_CXW.csv",True)
# plot_stock_filename("NYSE:GEO","STOCK_US_XNYS_GEO.csv",False)
# plot_stock_filename("NYSE:CXW","STOCK_US_XNYS_CXW.csv",False)