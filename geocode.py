import pgeocode
import csv
import json

nomi = pgeocode.Nominatim('us')

zipc_latlon = {}

def geocache(inputfile):
    with open(inputfile) as file:
        # with open(outputfile, "w") as output:
        reader = csv.reader(file)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            zipc = row[-1][:5]

            # print()
            # q =  # + "," + row[6]
            loc = nomi.query_postal_code(zipc)

            # print(loc)
            # print(f'{zipc},{loc.latitude},{loc.longitude}\n')
            
            # print(str(loc.latitude).upper())

            if str(loc.latitude).upper() == "NAN":
                zipc = ("0" + zipc)[:5]
                loc = nomi.query_postal_code(zipc)
                if str(loc.latitude).upper() == "NAN":
                    print("Not found :(")
                
            zipc_latlon[zipc] = [loc.latitude, loc.longitude]
                # output.write(f'{zipc},{loc.latitude},{loc.longitude}\n')

geocache("treemap - cbp.csv")
geocache("treemap - ice.csv")

with open("zipc_latlon.json","w") as out:
    json.dump(zipc_latlon, out)