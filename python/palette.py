import matplotlib.pyplot as plt
import seaborn as sns
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