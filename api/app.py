
from flask import Flask, request, jsonify, Response
import json, requests, os, sqlite3
from collections import OrderedDict
import operator, urllib, sys, tinys3
from boto.s3.connection import S3Connection

APIKEY =""
S3_ACCESS_KEY = ""
S3_SECRET_KEY = ""

#----------HELPER FUNCTIONS----------------
def getJSON(incomingRequest):
    requestBody =  json.loads((incomingRequest).decode("utf-8"))
    return requestBody

def getBills(customerID):
    url = "http://api.reimaginebanking.com/customers/" + customerID + "/bills?"
    url = url + urllib.urlencode(APIKEY)
    response = requests.get(url)
    return json.loads(response.content)

def getSubscriptions(responseBody):
    return responseBody.get("recurring_date")

def createSubscription(subName, body):
    filename = subName + ".json"
    with open(filename,"w") as f:
        json.dump(body, f)
    return filename

def uploadToS3Account(userName, filename):
    conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)
    f = open(filename,'rb')
    conn.upload("/users/" + userName + "/" + filename,f,'substop')
    f.close()

def updateSubscription(subName, userName, date):
    if(os.path.isfile("/users/" + userName + "/" + subName + ".txt") == False):
        return
    filename = subname + ".txt"
    f = open(filename, "w")
    f.write(date)
    f.close()
    return filename

def getCustomerID(username):
    response = requests.get("https://s3.amazonaws.com/substop/users/" + username + "/ACCOUNT.json")
    return response.json().get("customerID")

#----------API FRAMEWORK/PROCCESSING-------------------
app = Flask(__name__)
@app.route("/")
def home():
    return "WELCOME TO SUBSTOP API! DOCUMENTATION COMING SOON"


@app.route("/setSubscriptions", methods = ['POST']) #username, body
def setSubscriptions():
    username = getJSON(request.data).get("username")
    ###CONFIGURE BODY
    body = getJSON(request.data)
    del body['username']
    for item in getBills(getCustomerID(username)):
        if "recurring_date" in item:
            body = {"date": "date"}
            filename = createSubscription(item.get("payee"), body)
            uploadToS3Account(username, filename)
            os.remove(filename)
    return Response(status = 200)

@app.route("/createAccount", methods = ['POST']) #username, body
def createAccount():
    username = getJSON(request.data).get("username")
    body =  getJSON(request.data)
    del body['username']
    with open("ACCOUNT.json","w") as f:
        json.dump(body, f)
    uploadToS3Account(username, "ACCOUNT.json")
    os.remove("ACCOUNT.json")
    return Response(status = 200)

@app.route("/updateSubscription", methods = ['POST']) #username, subname, body
def updateSubscription():
    username = getJSON(request.data).get("username")
    subname = getJSON(request.data).get("subname")
    body = getJSON(request.data)
    del body['username']
    del body['subname']
    filename = createSubscription(subname, body)
    uploadToS3Account(username, filename)
    os.remove(filename)
    return Response(status = 200)

@app.route("/checkSubscription/<username>/<subname>") #username, subname
def checkSubscription(username, subname):
    response = requests.get("https://s3.amazonaws.com/substop/users/" + username + "/" +subname + ".json")
    return response.json().get("date")




#-------------------APP EXECUTION--------------------------
if __name__ == "__main__":
    app.run(debug = True)
