import csv
import bpy
import math


def get_data_from(filename):
    dic = []
    # dictt = {}
    
    with open(filename) as file:
        areas = csv.reader(file)
        # header = next(areas) # it has no header
        
        for area in areas:
            dic.append(list(map(int,area[1:-2])))
        return dic

path = "C:\\Users\\aliha\\Desktop\\immigration-border-misc\\python\\jon_data.csv"
raw_data = get_data_from(path)

#print("\n".join([f"cbp:{rd[0]},ice:{rd[1]},+:{sum(rd[:2])},box:{sum(rd[:2])/4558:2.3f},leftover:{sum(rd[:2]) % 4558:2.3f}" for rd in raw_data]))
cbp = []
ice = []
totals = []
n_boxes = [] 
leftovers = []
BOX = 4558

for rd in raw_data:
    cbp.append(rd[0])
    ice.append(rd[1])
    totals.append(cbp[-1] + cbp[-2])
    n_boxes.append(totals[-1] // BOX)
    leftovers.append(totals[-1] % BOX)

i = 0

cube = bpy.data.objects["basebox"]
txt = cube.children["label"]

cc = bpy.data.collections.new("temp")


for t, nb, l in zip(totals, n_boxes, leftovers):
    i += 1
    nc = cube.copy()
    cc.objects.link(nc)
    # nc.set
    
