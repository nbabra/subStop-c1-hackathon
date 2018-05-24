$(document).ready(function () {
    chrome.tabs.getSelected(null, function(tab) {
        var link = document.createElement("a"); 
        link.href = tab.url; 
        $('#host').html("Host: " + link.hostname); 
    })

})

