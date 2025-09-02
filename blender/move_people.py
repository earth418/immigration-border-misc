#import blender as bpy
# import bpy
import csv
import bpy
import math


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

def latlon_to_world(lat, lon, R=60):
    x = R * (lon - 0.0)
    y = R * math.log(math.tan(math.pi / 4.0 + lat / 2.0))
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

graph = bpy.context.evaluated_depsgraph_get()
people = bpy.data.objects["dude"]
e_people = people.evaluated_get(graph)

instances = (p for p in graph.object_instances if p.is_instance and p.parent == e_people)

#print([i.get('id') for i in instances])
print(next(instances).id_data)
#print(instances)
1/0

priv_count = priv_index = 0
pub_count = pub_index = 0

for instance in instances:
    
    instance.keyframe_insert(data_path="location",frame=128)
        
    if instance.get('id') == 0: # 5396 of them
        p = privs[priv_index]
        priv_count += 1
        if priv_count == p[0]:
            priv_index += 1
            priv_count = 0
        
        # priv_count += p[0]
        instance.location = latlon_to_world(p[1], p[2])
        # instance.location = (10.0, 10.0, 0.0)
        
    else:
        p = pubs[pub_index]
        pub_count += 1
        if pub_count == p[0]:
            pub_index += 1
            pub_count = 0

        instance.location = latlon_to_world(p[1], p[2])
    
    instance.keyframe_insert(data_path="location",frame=196)
    
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