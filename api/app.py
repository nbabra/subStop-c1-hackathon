from flask import Flask, request, jsonify
import json, requests, os, sqlite3
from collections import OrderedDict
import operator, urllib
APIKEY = { 'key': '7ab1c5c2151720f0b4104d7a9a2d7b9f'}
#----------HELPER FUNCTIONS----------------
def getJson(incomingRequest):
    requestBody =  json.loads((incomingRequest).decode("utf-8"))
    return requestBody
def getResponseContent(response):
    return response[1: len(response) -1]
def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print ("URL format error!")
def analyze(results):
    prompt = input("[.] Type <c> to print or <p> to plot\n[>] ")
    if prompt == "c":
        # print(results.items())
        for site, count in results.items():
            print (site, count)
    elif prompt == "p":
        plt.bar(range(len(results)), results.values(), align='edge')
        plt.xticks(rotation=45)
        plt.xticks(range(len(results)), results.keys())
        plt.show()
    else:
        print ("[.] Uh?")
        quit()

def getHistory():
    #path to user's history database (Chrome)
    data_path = os.path.expanduser('~').replace("\\", "\\\\")
    data_path = data_path + ("\\AppData\\Local\\Google\Chrome\\User Data\\Default") #.replace("\\", "\\\\")
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, 'history')
    #querying the db
    c = sqlite3.connect(history_db)
    cursor = c.cursor()
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    # print (results )
    # return "200"
    sites_count = {} #dict makes iterations easier :D
    for url, count in results:
        url = parse(url)
        if url in sites_count:
            sites_count[url] += 1
        else:
            sites_count[url] = 1
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
    analyze (sites_count_sorted)
    print("200")
    rawStringJson = (str(dict(sites_count_sorted.items()))).replace("'", '"')
    print(rawStringJson)
    return rawStringJson

def getBills(customerID):
    url = "http://api.reimaginebanking.com/customers/" + customerID + "/bills?"
    url = url + urllib.urlencode(APIKEY)
    response = requests.get(url)
    return getResponseContent(response.content)

#
#
# def getSubscriptions():


#----------API FRAMEWORK/PROCCESSING-------------------
app = Flask(__name__)
@app.route("/")
def home():
    return "Hello World!"

@app.route("/getHistory", methods = ['POST'])
def helloWorld():
    returnObject =  jsonify(getHistory())
    print('FJKS:DFJSKD:FJKSD:FJKS:D')
    print (returnObject.data())
    return returnObject

@app.route("/getSubscriptions/<customerID>")
def getAccount(customerID):
    print getBills(customerID)
    print ""
    return jsonify([getBills(customerID)])



#-------------------APP EXECUTION--------------------------
if __name__ == "__main__":
    app.run(debug = True)
