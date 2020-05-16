from uszipcode import SearchEngine, SimpleZipcode, Zipcode
from radar import RadarClient
import googlemaps
import requests

#uszipcode zipcode collection
search = SearchEngine()
res = search.by_state("California",returns=1601)
coords = []
for r in res:
    coords += [(r.zipcode,r.lat,r.lng)]

#API keys
radar = RadarClient('prj_test_sk_a014dc93fd7af85ef7ae08dba757a3316987e979')
maps = googlemaps.Client(key='AIzaSyB-3lXIqJLkzN-Wjb2twA2WaNJKLkc6Ybo')

#mongo data collection storage
forUpload = []

for c in coords:
    ser = (c[1],c[2])

    search = radar.search.places(near=ser,categories=["hotel-lodging","food-beverage","commercial-industrial","arts-entertainment","shopping-retail"])
    for s in search:
        name = s.name
        addr = radar.search.autocomplete(name, near=ser)
        if len(addr) > 0:
            if any(char.isdigit() for char in addr[0].formattedAddress):
                mapsS = maps.places(name,location=ser)
                placeId = mapsS['results'][0]['place_id']
                dets = maps.place(placeId)
                phone = dets['result']['international_phone_number']
                phone = phone.replace(' ','')
                phone = phone.replace('-','')
                faddr = addr[0].formattedAddress
                forUpload+=[(name,phone,faddr,placeId,ser)]
                print(forUpload)

#name #international_phone_number #addr #placeId #coords
