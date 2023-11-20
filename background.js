chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.message === "summarize") {
        // Send the text to the Flask server
        fetch('http://your-flask-server-endpoint/summarize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: request.text }),
        })
        .then(response => response.json())
        .then(summary => {
          // Handle the summary received from the server
          console.log('Summary:', summary);
  
          // You can now do something with the summary, like displaying it in a notification
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'path-to-your-icon/icon.png',
            title: 'Text Summarized!',
            message: summary,
          });
        })
        .catch(error => {
          console.error('Error:', error);
        });
      }
    }
  );