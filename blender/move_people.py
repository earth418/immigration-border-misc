#import blender as bpy
# import bpy
import csv
import bpy
import math
import random

def random_circle(R=1):
    a = random.random() * 2 * math.pi
    r = R * random.random()
    return (r * math.cos(a), r * math.sin(a))

def get_data_from(filename):
    privates = []
    publics = []
    
    with open(filename) as file:
        prisonfile = csv.reader(file)
#        print(next(prisonfile)) # csv header
        next(prisonfile)
        
        for prison in prisonfile:
            # print(prison)
            if prison[5] == "TRUE":
                privates.append(prison)
            else:
                publics.append(prison)

    return privates, publics

def latlon_to_world(lat : float, lon : float, R=600):
    us_lat = 37 * math.pi / 180.0
    us_lon = -95 * math.pi / 180.0
    x = R * (lon - us_lon)
    y = R * math.log(math.tan(math.pi / 4.0 + (lat - us_lat) / 2.0))
    return (x, y, 0.0)

path = "C:\\Users\\aliha\\Desktop\\immigration-border-misc\\blender\\AUG2025_DetentionCenters.csv"
privates, publics = get_data_from(path)

# total = 0
privs = []
for private in privates:
    i = math.ceil(1.4 * int(private[8].replace(",","")) / 10) # 5394
    privs.append([
        i,
        private[10],
        private[11],
    ])
    # total += i
# print(total)

# We have 2 guys still unassigned
privs[0][0] += 1
privs[1][0] += 1


# total_pub = 0
pubs = []
for public in publics:
    i = math.ceil(0.7 * int(public[8].replace(",","")) / 10) # 603
    pubs.append([
        i,
        float(public[10]),
        float(public[11]),
    ])
    # total_pub += i
# print(total_pub)

priv_count = priv_index = 0
pub_count = pub_index = 0



pc = bpy.data.objects["test_data"]
old_mesh = pc.data
mesh = bpy.data.meshes.new("mesh1")
pc.data = mesh
bpy.data.meshes.remove(old_mesh)

locations1 = []
i = 0
while i < 5396: # 5396 of them
    print(priv_index)
    i += 1
    p = privs[priv_index]
    priv_count += 1
    
    if priv_count == p[0]:
        priv_index += 1
        priv_count = 0

    loc1 = latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180)
    rc = random_circle(3)
    loc = (loc1[0] + rc[0], loc1[1] + rc[1], loc1[2])
    locations1.append(loc)

mesh.from_pydata(locations1, [], [])
mesh.update()


pc = bpy.data.objects["test_data2"]
old_mesh = pc.data
mesh = bpy.data.meshes.new("mesh2")
pc.data = mesh
bpy.data.meshes.remove(old_mesh)

#mesh = .data
#mesh.clear_geometry()
locations2 = []

i = 0
while i < 603:
    i += 1
    p = pubs[pub_index]
    pub_count += 1
    if pub_count == p[0]:
        pub_index += 1
        pub_count = 0

        # locations2.append(latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180))
    loc2 = latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180)
    rc = random_circle(3)
    loc = (loc2[0] + rc[0], loc2[1] + rc[1], loc2[2])
    locations2.append(loc)
        
mesh.from_pydata(locations2, [], [])
mesh.update()


    # instance.instance_object.keyframe_insert(data_path="location",frame=196)
    # instance.keyframe_insert(data_path="location",frame=196)


#print(pubs[0])
#1/0

# bpy.ops.anim.change_frame(frame = 128)
# graph = bpy.context.evaluated_depsgraph_get()
# people = bpy.data.objects["dude"]
# e_people = people.evaluated_get(graph)


# e_people.data.attributes

# instances = (p for p in graph.object_instances if p.is_instance and p.parent == e_people)

# print(instances)
# next(instances).
# print(next(instances).instance_object.data.attributes.keys())
# 1/0

#print([i.get('id') for i in instances])
#for instance in instances:
#    print(instance.values())
#print(next(instances).instance_object.get('id'))
#1/0

# priv_count = priv_index = 0
# pub_count = pub_index = 0
# i = 0


# for instance in instances:
    
#     # instance.instance_object.keyframe_insert(data_path="location",frame=128)
#     instance.keyframe_insert(data_path="location",frame=128)
# #    i += 1        
# #    if i < 5396: # 5396 of them
    
#     if instance.instance_object.data.attributes["private"]:
#         print(priv_index)
#         p = privs[priv_index]
#         priv_count += 1
        
#         if priv_count == p[0]:
#             priv_index += 1
#             priv_count = 0
            
#             # priv_count += p[0]
#     #        print(p[1], p[2])
#             locations1.append(latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180))
#             instance.instance_object.location = latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180)
#             # instance.location = (10.0, 10.0, 0.0)
        
#     else:
#         p = pubs[pub_index]
#         pub_count += 1
#         if pub_count == p[0]:
#             pub_index += 1
#             pub_count = 0

#             instance.instance_object.location = latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180)
#             locations2.append(latlon_to_world(float(p[1]) * math.pi / 180, float(p[2]) * math.pi / 180))
    
#     # instance.instance_object.keyframe_insert(data_path="location",frame=196)
#     instance.keyframe_insert(data_path="location",frame=196)
    
# print(instances)






'''
Name,
City,
State,
Zip,
"Type Detailed*",
Private,
Operator,
"Current Guaranteed Minimum",
"Average Daily Population",
"Current as of**",
"Geocodio Latitude",
"Geocodio Longitude",
"Geocodio Accuracy Score",
"Geocodio Accuracy Type",
"Geocodio Address Line 1",
"Geocodio Address Line 2",
"Geocodio Address Line 3",
"Geocodio House Number",
"Geocodio Street",
"Geocodio Unit Type",
"Geocodio Unit Number",
"Geocodio City",
"Geocodio State",
"Geocodio County",
"Geocodio Postal Code",
"Geocodio Country",
"Geocodio Source"
'''


# print(instances)