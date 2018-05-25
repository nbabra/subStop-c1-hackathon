var matchedName = null; 
var userID = null; 

//get href 
var firstHref = $("a[href^='http']").eq(0).attr("href");


function createAccount() {

    var createAccountUrl = "https://276a4e99.ngrok.io/createAccount"; 
    var name = "testUser"; 
    var customerId = document.getElementById("customerNum"); 
    var phoneNumber  = document.getElementById("phonenumberField"); 
    
    alert("sTUFF HAPPENED")
    console.log(customerId); 
    console.log(phoneNumber);

    var xhr = new XMLHttpRequest();
        var url = createAccountUrl;
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("SUCCESS POST REQUEST");
            var json = JSON.parse(xhr.responseText);
            console.log(json);
        }
        };

        var data = JSON.stringify({"username": name, "customerID": customerId, "phone":phoneNumber});
        xhr.send(data);




} 
var parser = document.createElement("a"); 

//create parser element
parser.href = firstHref; 

//call function to parse  the url string
createNewParser(parser); 

//function to parse url into different elements
function createNewParser(newParser) {

    newParser.protocol; // => "http:"
    newParser.hostname; // => "example.com"
    newParser.port;     // => "3000"
    newParser.pathname; // => "/pathname/"
    newParser.search;   // => "?search=test"
    newParser.hash;     // => "#hash"
    newParser.host;     // => "example.com:3000"

    console.log("Host Name: " + newParser.hostname);  

    returnHostName(newParser.hostname);

    parseUrlString(newParser.hostname);
} 

function returnHostName(name) {
    return name; 
}

function parseUrlString(url) {

    //regex pattern to match    
    var regex = /\.(.*?)\./;

    var urlToMatch = String(url);

    matchedName = String(regex.exec(urlToMatch)[1]);

    console.log("Parsed: " + matchedName);

}

makePost(matchedName);

//make http request to api and check if this is a subscription (true or false)
function makePost(currentSite) {

    /*check if parameter is a subscription - query api

    *NO - ignore - dont send any message or notify user
    *YES -->
        *Get # times visited from api
        *update that value 
        *
    */

    //create request url for http request

    var userName = "testUser" //update later


    
    var updateSubscription = "updateSubscription"
    var requestUrl = "https://276a4e99.ngrok.io/"; 
    var postRequestUrl = "https://276a4e99.ngrok.io/" + updateSubscription; 
    var currentDate = Date.now(); 

    console.log("POST URL: " + postRequestUrl);

    var xhr = new XMLHttpRequest();
        var url = postRequestUrl;
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("SUCCESS POST REQUEST");
            var json = JSON.parse(xhr.responseText);
            console.log(json);
        }
        };

        var data = JSON.stringify({"username": userName, "subname": currentSite, "date": String(currentDate)});
        xhr.send(data);


    getDateFromGet(requestUrl, userName, currentSite); 

}

function getDateFromGet(partialRequestURL, usernameAcc, subname) { 

    var checkSubscription = "checkSubscription";

    var dateRequestUrl = partialRequestURL + checkSubscription + "/" + usernameAcc + "/" + subname;


    console.log("GET URL: " + dateRequestUrl);

    var authHeader = "auth header";

    $.ajax({
        url: dateRequestUrl,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            console.log("GET REPSONSE: " + res);
            //alert(res);
            checkForNotificationDisplay(res, subname);             
        }
    });
}

//checks if a notification should be sent 
function checkForNotificationDisplay(getResponse, subname) {
    //subtract reponse date value from current date time value 

    var currentDateTime = Date.now()//returns UTC value 

    var visitedTime = getResponse; 

    var thresholdValue = 2592000; 

    if ((currentDateTime - visitedTime) > thresholdValue) { 

        
        var sendText = "sendText"; 
        var textRequestUrl = "https://276a4e99.ngrok.io/" + sendText; 

        //send text to user 
        var xhr2 = new XMLHttpRequest();
        var url2 = textRequestUrl;
        xhr2.open("POST", url2, true);
        xhr2.setRequestHeader("Content-Type", "application/json");
        xhr2.onreadystatechange = function () {
        if (xhr2.readyState === 4 && xhr2.status === 200) {
            console.log("SUCCESS POST REQUEST FOR TEXT");
            var json = JSON.parse(xhr2.responseText);
            console.log(json);
        }
        };

        //only takes user name
        var data = JSON.stringify({"username": userName});
        xhr2.send(data);

    //---------------------------------------------------------------------------------
        var updateSubscription = "updateSubscription"; 
        var postRequestUrl = "https://276a4e99.ngrok.io/" + updateSubscription; 
        var userName = "testUser"; 

        //make another POST Request to update the date field with the new value (current time)
         

                var xhr = new XMLHttpRequest();
                var url = postRequestUrl;
                xhr.open("POST", url, true);
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    console.log("SUCCESS POST REQUEST");
                    var json = JSON.parse(xhr.responseText);
                    console.log(json);
                }
                };

                var data = JSON.stringify({"username": userName, "subname": subname, "date": String(currentDateTime)});
                xhr.send(data);
    }
    
}   


//----EVERY 45 DAYS - AWS LAMBDA FUNCTIONALITY----
/*
    *tell user how many times they've visited this site/service
    *if number below certain threshold - reccommend to user that they should consider unsubscribing
        --we should ideally only recommend if they havent already unsubscribed
        --should send email to the user at this three month mark detailing the reccomendation
    *clear the logged data and send back to server
*/ 
 