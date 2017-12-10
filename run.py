# import all the libraries we will be using
from flask import Flask, request
from twilio import twiml

# set up Flask to connect this code to the local host, which will
# later be connected to the internet through Ngrok
app = Flask(__name__)

# Main method. When a POST request is sent to our local host through Ngrok
# (which creates a tunnel to the web), this code will run. The Twilio service
# sends the POST request - we will set this up on the Twilio website. So when
# a message is sent over SMS to our Twilio number, this code will run.
@app.route('/', methods=['POST'])
def sms():
    # Get the text in the message sent
    message_body = request.form['Body']

    # Create a Twilio response object to be able to send a reply back (as per
    # Twilio docs)
    resp = twiml.Response()

    # Send the message body to the getReply message, where
    # we will query the String and formulate a response
    replyText = getReply(message_body)

	# Text back our response!
    resp.message('Hi\n\n' + replyText)
    return str(resp)

# when you run the code through terminal, this will allow Flask to work
if __name__ == '__main__':
    app.run()

""" Now we need to create a getReply method. This method will simply look
    through our text message body and figure out the type of information we
    want. It will then get the information from different APIs and return a
    response. Assuming our text message will be formatted as "keyword_request,"
    a simple format that we can use to identify what is requested in the
    message is as follows:
"""

def getReply(message):
    """Function to formulate a response based on message input."""
    message = message.lower().strip()
    # This is the variable where we will store our response.
    answer = ""

    if "weather" in message:
        answer = "get the weather using a weather API"

    # is the keyword "wolfram" in the message? e.g., "wolfram integral of x+1"
    elif "wolfram" in message:
        answer = "get a response from the Wolfram Alpha API"

    # is the keyword "wiki" in the message? e.g., "wiki donald trump"
    elif "wiki" in message:
        # remove the keyword "wiki" from the message
        message = removeHead(message, "wiki")

        # Get the wikipedia summary for the request
        try:
            # Get the summary off Wikipedia
            answer = wikipedia.summary(message)
        except:
            # handle errors or non-specificity errors (e.g., too many results)
            answer = "Request was not found using wiki. Be more specific?"
        
    
    # is the keyword "some_keyword" in the message? You can create your own custom
    # requests! e.g., "schedule Monday"
    elif "some_keyword" in message:
        answer = "some response"
    
    # the message contains no keyword. Display a help prompt to identify possible
    # commands
    else:
        answer = "\n Welcome! These are the commands you may use: \nWOLFRAM \"wolfram alpha request\" \nWIKI \"wikipedia request\" \nWEATHER \"place\" \nSOME_KEYWORD \"some custom request\"\n"
    
    # Twilio can not send messages over 1600 characters in one message. Wikipedia 
    # summaries may have way more than this, so shortening is required:
    if len(answer) > 1500:
        answer = answer[0:1500] + "..."

    # return the formulated answer
    return answer

""" Now our message format is as follows: "Keyword_request". However, you cannot
    put in "wolfram calories in bread" into wolfram alpha. However, you can put
    in "calories in bread". So now we have to take out "wolfram" from the message
    to isolate the request. We can do so with the following method:
"""
# Function for editing input text to remove keyword from search terms.
def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()
    
    return fromThis

""" It’s time to put in the APIs. We will be using Wolfram Alpha, Wikipedia,
    and yWeather. All have amazing documentation online, so I won’t be going
    much into how to formulate each "if statement" in the getReply method. For
    Wolfram Alpha you will need to go to their API site to get an API key.
    Wikipedia and yWeather do not require keys.
    Let’s set up the Wikipedia API. Go to terminal and type in "pip install
    wikipedia". Now go to the Wikipedia if statement in the getReply method
    and add the following:
"""

