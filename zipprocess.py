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
