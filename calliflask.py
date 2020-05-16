from flask import Flask, render_template, request, send_file
import mongo

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def home():

    return render_template("front.html")

@app.route("/call",methods=['GET', 'POST'])
def call():
    m = mongo.randomDB(mongo.connectMongo())
    #ADD ONLY if OPEN
    return render_template("callpage.html", phone=m['phone'])

if __name__ == "__main__":
    app.run(debug=True)
