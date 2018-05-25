
from flask import Flask, request, jsonify, Response, render_template
from flask_mail import Mail, Message
import json, requests, os, sqlite3
from collections import OrderedDict
import operator, urllib, sys, tinys3
import smtplib


APIKEY = { 'key': ''}
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
    conn.upload("/users/" + userName + "/" + filename,f,'substopv2')
    f.close()

def updateSubscription(subname, userName, body):
    response = requests.get("https://s3.us-east-2.amazonaws.com/substopv2/users/" + userName + "/" + subname.lower() + ".json")
    if(response.status_code != 200):
        print "postpajtdjfidasopjfisapdji"
        return "NULL"
    filename = subname.lower() + ".json"
    with open(filename, "w") as f:
        json.dump(body, f)
    return filename

def getCustomerID(username):
    response = requests.get("https://s3.us-east-2.amazonaws.com/substopv2/users/" + username + "/ACCOUNT.json")
    temp = json.loads(response.content)
    return temp.get("customerID")

def getPhoneNumber(username):
    response = requests.get("https://s3.us-east-2.amazonaws.com/substopv2/users/" + username + "/ACCOUNT.json")
    temp = json.loads(response.content)
    return temp.get("phone")

#----------API FRAMEWORK/PROCCESSING-------------------
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('login-page.html')

@app.route("/thank-you")
def load():
    body = "{'username':'testUser', 'customerID':'5b0439bd322fa06b677939e8', 'phone':'6306052697'}"
    data = json.loads(body)
    response = requests.post("http://3676dca2.ngrok.io/createAccount", data)
    return render_template('thank-you.html')


@app.route("/setSubscriptions", methods = ['POST']) #username, body  GETS all subscriptions
def setSubscriptions():
    username = json.loads(request.data).get("username")
    ###CONFIGURE BODY
    body = json.loads(request.data)
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
    print request.data
    username = json.loads(request.data).get("username")
    body =  json.loads(request.data)
    print request.data
    del body['username']
    with open("ACCOUNT.json","w") as f:
        json.dump(body, f)
    uploadToS3Account(username, "ACCOUNT.json")
    os.remove("ACCOUNT.json")
    return Response(status = 200)

@app.route("/updateSubscription", methods = ['POST']) #username, subname, body(date and phone number whatever else)
def updateSubscriptions():
    print request.data
    username = json.loads(request.data).get("username")
    subname = json.loads(request.data).get("subname")
    subname = subname.lower()
    body = getJSON(request.data)
    del body['username']
    del body['subname']
    filename = updateSubscription(subname, username, body)
    if(filename=="NULL"):
        return Response(status = 200)
    uploadToS3Account(username, filename)
    os.remove(filename)
    return Response(status = 200)

@app.route("/checkSubscription/<username>/<subname>") #username, subname #returns date
def checkSubscription(username, subname):
    response = requests.get("https://s3.us-east-2.amazonaws.com/substopv2/users/" + username + "/" +subname.lower() + ".json")
    return response.json().get("date")

@app.route("/sendText", methods = ['POST'])
def sendText():
    username = getJSON(request.data).get("username")
    server = smtplib.SMTP( "smtp.gmail.com", 587 )

    server.starttls()

    server.login( 'substop18@gmail.com', 'substop123' )

    # Send text message through SMS gateway of destination number
    phonePath = getPhoneNumber(username) + "@pm.sprint.com"
    server.sendmail( '2405352040', phonePath, 'Check Subscription! You have unused Subscription payments!')

    return Response(status = 200)


#-------------------APP EXECUTION--------------------------
if __name__ == "__main__":
    app.run(debug = True, port = 80)
