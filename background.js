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

    matchedName = String(regex.exec(urlToMatch)[1]);

    console.log("Parsed: " + matchedName);

}

//checks if valid url
// if (matchedName != null) {

//     makePost(matchedName); //netflix, amazon
// } else {
//     console.log("Error! Invalid URL");
// }

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
    var requestUrl = "https://94db0f79.ngrok.io/"; 
    var postRequestUrl = "https://94db0f79.ngrok.io/" + updateSubscription; 
    var currentDate = Date.now(); 

    // $.post(requestUrl,

    // {
    //     username: userName, //i.e "Johnn"
    //     subname:  currentSite, //i.e. Netflix
    //     body:  String(currentDate) 

    // },

    // function(data,status){
         
    //     alert("Data: " + data + "\nStatus: " + status);
    //     console.log(data);

    // });


    console.log("POST URL: " + postRequestUrl);

    // $.ajax({
    //     url: postRequestUrl,
    //     type: 'post',

    //     data: {
    //         "username" : userName, //i.e "Johnn"
    //         "subname" :  currentSite, //i.e. Netflix
    //         "date" :  String(currentDate) 
    //     },
    //     // headers: {

    //     //     "Content-Type": "application/json",

    //     // },

    //     dataType: 'json',

    //     success: function (data) {
    //         console.log(data);
    //     }
    // });


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

    var checkSubscription = "checkSubscription"

    var dateRequestUrl = partialRequestURL + checkSubscription + "/" + usernameAcc + "/" + subname;


    console.log("GET URL: " + dateRequestUrl);

//     $.get(dateRequestUrl,
//           // url
//     function (data, textStatus, jqXHR) {  // success callback
        
//         alert('status: ' + textStatus + ', data:' + data); //do something with the data

//         console.log(textStatus);
//   });

    var authHeader = "auth header";

    $.ajax({

        url: dateRequestUrl,

        data: { signature: authHeader },
        type: "GET",

        beforeSend: function(xhr){xhr.setRequestHeader('X-Test-Header', 'test-value');},

        success: function() { 
            console.log('Success! ' + authHeader);
            alert('Success!' + authHeader); 
        }

    });
}

    function checkForNotificationDisplay() {
        
    }

//----EVERY 45 DAYS - AWS LAMBDA FUNCTIONALITY----
/*
    *tell user how many times they've visited this site/service
    *if number below certain threshold - reccommend to user that they should consider unsubscribing
        --we should ideally only recommend if they havent already unsubscribed
        --should send email to the user at this three month mark detailing the reccomendation
    *clear the logged data and send back to server
*/ 
 