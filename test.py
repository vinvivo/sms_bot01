from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import wikipedia

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent to our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the appropriate reply for this message
    replyText = getReply(body)

    # if body == 'hello':
    #     resp.message("Hi!")
    # elif body == 'bye':
    #     resp.message("Goodbye")
    # else:
    #     resp.message("I'm sorry. I don't know how to respond to that.")
    
    resp.message('Hi\n\n' + replyText)

    return str(resp)

def getReply(message):
    """Function to formulate a response based on message input."""
    message = message.lower().strip()
    # This is the variable where we will store our response.
    answer = ""

    if "hello" in message:
        answer = "hi!"
    
    elif "bye" in message:
        answer = "Goodbye!"

    elif "wiki" in message:
        # remove the keyword "wiki" from the message
        message = removeHead(message, "wiki")

        # Get the wikipedia summary for the request
        try:
            answer = wikipedia.summary(message)
        except:
            answer = "Request was not found using wiki. Be more specific?"
    
    else:
        answer = "\n Welcome! These are the commands you may use: \nWOLFRAM \"wolfram alpha request\" \nWIKI \"wikipedia request\" \nWEATHER \"place\" \nSOME_KEYWORD \"some custom request\"\n"
    
    if len(answer) > 1500:
        answer = answer[0:1500] + "..."
    
    return answer

def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()
    
    return fromThis

if __name__ == "__main__":
    app.run(debug=True)
