
from flask import Flask, request, jsonify, Response
import json, requests, os, sqlite3
from collections import OrderedDict
import operator, urllib, sys, tinys3
import boto3
from boto.s3.connection import S3Connection

APIKEY = { 'key': 'e705696f2fdd186ff04c68829075d30c'}
S3_ACCESS_KEY = "AKIAJS5SXHI5J3QQLDEA"
S3_SECRET_KEY = "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"
#----------HELPER FUNCTIONS----------------
def getJSON(incomingRequest):
    requestBody =  json.loads((incomingRequest).decode("utf-8"))
    return requestBody

def getBills(customerID):
    url = "http://api.reimaginebanking.com/customers/" + customerID + "/bills?"
    url = url + urllib.urlencode(APIKEY)
    response = requests.get(url)
    print response
    return json.loads(response.content)

def getSubscriptions(responseBody):
    return responseBody.get("recurring_date")

def createSubscription(subName, body):
    filename = subName.lower() + ".json"
    with open(filename,"w") as f:
        json.dump(body, f)
    return filename

def uploadToS3Account(userName, filename):
    conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)
    f = open(filename,'rb')
    conn.upload("/users/" + userName + "/" + filename,f,'substop18')
    f.close()

def updateSubscription(subname, userName, body):
    response = requests.get("https://s3-us-west-1.amazonaws.com/substop18/users/" + userName + "/" + subname.lower() + ".json")
    if(response.status_code != 200):
        print "postpajtdjfidasopjfisapdji"
        return "NULL"
    filename = subname.lower() + ".json"
    with open(filename, "w") as f:
        json.dump(body, f)
    return filename

def getCustomerID(username):
    response = requests.get("https://s3-us-west-1.amazonaws.com/substop18/users/" + username + "/ACCOUNT.json")
    temp = json.loads(response.content)
    return temp.get("customerID")

#----------API FRAMEWORK/PROCCESSING-------------------
app = Flask(__name__)
@app.route("/")
def home():
    return "WELCOME TO SUBSTOP API! DOCUMENTATION COMING SOON"


@app.route("/setSubscriptions", methods = ['POST']) #username, body  GETS all subscriptions
def setSubscriptions():
    username = getJSON(request.data).get("username")
    ###CONFIGURE BODY
    body = getJSON(request.data)
    del body['username']
    for item in getBills(getCustomerID(username)):
        print item
        if "recurring_date" in item:
            filename = createSubscription(item.get("payee"), body)
            uploadToS3Account(username, filename)
            os.remove(filename)
    return Response(status = 200)

@app.route("/createAccount", methods = ['POST'])
def createAccount():
    username = getJSON(request.data).get("username")
    body =  getJSON(request.data)
    del body['username']
    with open("ACCOUNT.json","w") as f:
        json.dump(body, f)
    uploadToS3Account(username, "ACCOUNT.json")
    os.remove("ACCOUNT.json")
    return Response(status = 200)

@app.route("/updateSubscription", methods = ['POST']) #username, subname, body(date and whatever else)
def updateSubscriptions():
    username = getJSON(request.data).get("username")
    subname = getJSON(request.data).get("subname")
    subname = subname.lower()
    body = getJSON(request.data)
    del body['username']
    del body['subname']
    filename = updateSubscription(subname, username, body)
    if(filename=="NULL"):
        return Response(status = 400)
    uploadToS3Account(username, filename)
    os.remove(filename)
    return Response(status = 200)

@app.route("/checkSubscription/<username>/<subname>") #username, subname #returns date
def checkSubscription(username, subname):
    response = requests.get("https://s3-us-west-1.amazonaws.com/substop18/users/" + username + "/" +subname.lower() + ".json")
    return response.json().get("date")

#-------------------APP EXECUTION--------------------------
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')
