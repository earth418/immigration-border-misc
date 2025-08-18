import pgeocode
import csv
import json
import requests

nomi = pgeocode.Nominatim('us')

zipc_latlon = {}

# https://geocoding.geo.census.gov/geocoder/locations/address?street=4600+Silver+Hill+Rd&city=Washington&state=DC&zip=20233&benchmark=Public_AR_Current&format=json

def geocache(inputfile):
    with open(inputfile) as file:
        # with open(outputfile, "w") as output:
        reader = csv.reader(file)
        first = True
        for row in reader:
            if first:
                first = False
                continue
            # zipc = row[-1][:5]

            # rq = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={"+".join(row[3].split(" "))}&city={row[4]}&state={row[6]}&zip={row[-1]}&benchmark=Public_AR_Current&format=json"
            rq = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={"+".join(row[3].split(" "))}&city={row[4]}&state={row[6]}&benchmark=Public_AR_Current&format=json"

            print(rq)
            res = requests.get(rq)
            J = json.loads(res.text)
            # j = json.decoder(res.text)
            print(J["result"])
            print(J["result"]["addressMatches"][0]["coordinates"])
            # print()
            # q =  # + "," + row[6]
            # loc = nomi.query_postal_code(zipc)

            # print(loc)
            # print(f'{zipc},{loc.latitude},{loc.longitude}\n')
            
            # print(str(loc.latitude).upper())

            # if str(loc.latitude).upper() == "NAN":
            #     zipc = ("0" + zipc)[:5]
            #     loc = nomi.query_postal_code(zipc)
            #     if str(loc.latitude).upper() == "NAN":
            #         print("Not found :(")
                
            # zipc_latlon[zipc] = [loc.latitude, loc.longitude]
                # output.write(f'{zipc},{loc.latitude},{loc.longitude}\n')

geocache("treemap - cbp.csv")
geocache("treemap - ice.csv")

# with open("zipc_latlon.json","w") as out:
#     json.dump(zipc_latlon, out)