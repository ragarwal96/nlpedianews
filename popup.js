
/* this code waits for a button called "summarizeButton" to be clicked on a web page. 
When it's clicked, it finds what page is open, and then sends a message to that page, 
asking it to summarize something */

document.addEventListener('DOMContentLoaded', function() {  //when the web page is fully loaded, do something!
    var summarizeButton = document.getElementById('summarizeButton'); //finding a button with label "summarizeButton" and remembering it as "summarizeButton."
    
    summarizeButton.addEventListener('click', function() { //when the summarize button is clicked, do something!
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) { //which page is currently active in the window?
        var activeTab = tabs[0]; //first page = active tab
        chrome.tabs.sendMessage(activeTab.id, {"message": "summarize"}); //telling the page to summarize
      });
    });
  });