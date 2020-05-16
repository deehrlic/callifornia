from uszipcode import SearchEngine, SimpleZipcode, Zipcode
from radar import RadarClient
import googlemaps
import requests
import mongo
import threading

#uszipcode zipcode collection
search = SearchEngine()
res = search.by_state("California",returns=1601)
coords = []
for r in res:
    coords += [(r.zipcode,r.lat,r.lng)]

#API keys
radar = RadarClient('prj_test_sk_a014dc93fd7af85ef7ae08dba757a3316987e979')
maps = googlemaps.Client(key='AIzaSyB-3lXIqJLkzN-Wjb2twA2WaNJKLkc6Ybo')
src = mongo.connectMongo()

#mongo data collection storage
forUpload = []

def addData(list,forUpload):

    print(list)
    for c in list:
        ser = (c[1],c[2])

        search = radar.search.places(near=ser,categories=["hotel-lodging","food-beverage","commercial-industrial","arts-entertainment","shopping-retail"])
        for s in search:
            name = s.name
            addr = radar.search.autocomplete(name, near=ser)
            if len(addr) > 0:
                if any(char.isdigit() for char in addr[0].formattedAddress):
                    mapsS = maps.places(name,location=ser)
                    if len(mapsS['results']) > 0:
                        placeId = mapsS['results'][0]['place_id']
                        dets = maps.place(placeId)
                        if 'international_phone_number' in dets['result']:
                            phone = dets['result']['international_phone_number']
                            phone = phone.replace(' ','')
                            phone = phone.replace('-','')
                            faddr = addr[0].formattedAddress
                            placeData = [(name,phone,faddr,placeId,ser)]
                            forUpload+=placeData
                            print(placeData)


t1 = threading.Thread(target=addData,args=(coords[120:130],forUpload))
t2 = threading.Thread(target=addData,args=(coords[230:240],forUpload))
t3 = threading.Thread(target=addData,args=(coords[440:450],forUpload))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
print(forUpload, len(forUpload))

for up in forUpload:
    mongo.addtoDB(up,src)
