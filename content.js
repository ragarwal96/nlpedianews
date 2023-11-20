/* when a web page sends a message that says "summarize," this code collects all the words
 from that page and sends them to another part of the extension that knows how to make a summary */

chrome.runtime.onMessage.addListener( //when you get message from page, do something!
    function(request, sender, sendResponse) { //setting up a special ear/place to listen
      if( request.message === "summarize" ) { //checks if message is asking for summary
        // Extract text from the webpage (you may need to customize this)
        var bodyText = document.body.innerText; //reading all the text on a page and putting it in bodyText
  
        // Send the text to the background script for summarization
        chrome.runtime.sendMessage({"message": "summarize", "text": bodyText}); //sends collected text to another part of the extension for summarizing
      }
    }
  );