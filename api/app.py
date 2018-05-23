from flask import Flask, request
import json, requests, jsonify


app = Flask(__name__)

def getJson(incomingRequest):
    requestBody =  json.loads((incomingRequest).decode("utf-8"))
    return requestBody

@app.route("/")
def home():
    return "Hello World!"

@app.route("/home", methods = ['POST'])
def helloWorld():
    return getJson(request.data).get("hello")

if __name__ == "__main__":
    app.run(debug = True)
