
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

    var matchedName = regex.exec(urlToMatch)[1];

    console.log("Parsed: " + matchedName);

}

function checkIfSubscription(currentSite) {

}

//get 