from flask import Flask, request
import json, requests, jsonify


APIKEY = 7ab1c5c2151720f0b4104d7a9a2d7b9f


#----------HELLPER FUNCTIONS----------------

def getJson(incomingRequest):
    requestBody =  json.loads((incomingRequest).decode("utf-8"))
    return requestBody


#----------API FRAMEWORK/PROCCESSING-------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/home", methods = ['POST'])
def helloWorld():
    return request.headers["Content-Type"]

if __name__ == "__main__":
    app.run(debug = True)
