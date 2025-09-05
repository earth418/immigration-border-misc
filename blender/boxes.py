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
    totals.append(cbp[-1] + ice[-1])
    n_boxes.append(totals[-1] // BOX)
    leftovers.append(totals[-1] % BOX)

# i = 0

cube = bpy.data.objects["basebox"]
#txt = cube.children["label"]
txt = cube.children[0]
totallabel = bpy.data.objects["total_label"]

cc = bpy.data.collections.new("temp")

# N = max(n_boxes)
side_length = lambda N: max(2, math.ceil(math.sqrt(N)))
scale_per_box = lambda N: 1.1 / side_length(N)
# offset = scale_per_box
pos = lambda N, nb: (-1.1 + scale_per_box(N) * (nb // side_length(N)), 
                      1.1 - scale_per_box(N) * (nb % side_length(N)))
# curr_nb = 1
curr_boxes = [cube] + [bpy.data.objects[f"basebox.{i:03d}"] for i in range(0,9)]

for i, (t, nb, l) in enumerate(zip(totals, n_boxes, leftovers)):
    
    
    totallabel.data.body = f'${t / 1000}B'
    for box in range(nb):
        if box >= len(curr_boxes):
            print("Error!!")
            # nc = cube.copy()
            # nc.data = cube.data.copy()
            # cc.objects.link(nc)
            # curr_boxes.append(nc)
    
        curr_box = curr_boxes[box]
        # curr_box.trans
        p = pos(nb, box)
        
        curr_box.keyframe_insert("location",frame=42+i*3)
        curr_box.keyframe_insert("location",frame=42+i*3)
        curr_box.location = p + (0.0,) # quick lil z axis action
        curr_box.keyframe_insert("location",frame=45+i*3)
        print(curr_box.location)
        
        if box == nb - 1:
            curr_box.scale = (l / BOX, l / BOX, curr_box.scale.z)
            
            curr_box.location = (p[0] - l, p[1] - l, 0.0)
            # pass
    # i += 1
        
