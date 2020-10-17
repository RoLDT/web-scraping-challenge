from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    Mars_Dict = mongo.db.Mars_Dict.find_one()
    return render_template("index.html", mars=Mars_Dict)


@app.route("/scrape")
def scraper():
    Mars_Dict = mongo.db.Mars_Dict
    Mars_data = scrape_mars.scrape()
    Mars_Dict.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)