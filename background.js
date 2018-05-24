var matchedName = null; 

//get href 
var firstHref = $("a[href^='http']").eq(0).attr("href");


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

    parseUrlString(newParser.hostname);
} 

function parseUrlString(url) {

    //regex pattern to match    
    var regex = /\.(.*?)\./;

    var urlToMatch = String(url);

    matchedName = regex.exec(urlToMatch)[1];

    console.log("Parsed: " + matchedName);

}

//checks if valid url
if (matchedName != null) {
    checkIfSubscription(matchedName); 
} else {
    console.log("Error! Invalid URL");
}



//make http request to api and check if this is a subscription (true or false)
function checkIfSubscription(currentSite) {

    /*check if parameter is a subscription - query api

    *NO - ignore - dont send any message or notify user
    *YES -->
        *Get # times visited from api
        *update that value 
        *
    */


}

//----EVERY 45 DAYS - AWS LAMBDA FUNCTIONALITY----
/*
    *tell user how many times they've visited this site/service
    *if number below certain threshold - reccommend to user that they should consider unsubscribing
        --we should ideally only recommend if they havent already unsubscribed
        --should send email to the user at this three month mark detailing the reccomendation
    *clear the logged data and send back to server
*/ 
 