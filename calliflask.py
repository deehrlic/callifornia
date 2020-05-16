from flask import Flask, render_template, request, send_file
import mongo
import googlemaps

app = Flask(__name__)

maps = googlemaps.Client(key='AIzaSyB-3lXIqJLkzN-Wjb2twA2WaNJKLkc6Ybo')

@app.route("/",methods=['GET', 'POST'])
def home():

    return render_template("front.html")

@app.route("/call",methods=['GET', 'POST'])
def call():
    isOpen = False
    while isOpen == False:
        m = mongo.randomDB(mongo.connectMongo())
        place = maps.place(m['placeId'])
        print(place)
        phone = m['phone']
        if 'reviews' in place['result']:
            texts = place['result']['reviews'][0]['text']
        else:
            texts = []
        #ONLY CALL OPEN PLACES
        if 'opening_hours' in place['result']:
            open = place['result']['opening_hours']['open_now']
            if open == True:
                url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(m['coords'][0])+","+str(m['coords'][1])+"&zoom=12&size=300x300&key=AIzaSyB-3lXIqJLkzN-Wjb2twA2WaNJKLkc6Ybo"
                return render_template("callpage.html", phone=phone, url=url)


if __name__ == "__main__":
    app.run(debug=True)
