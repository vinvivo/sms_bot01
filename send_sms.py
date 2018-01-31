from twilio.rest import Client

account_sid = "ENTER ACCOUNT SID HERE"
auth_token = "ENTER AUTH_TOKEN HERE"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to = "ENTER PHONE NUMBER HERE",     # +1234567890 format
    from_ = "+14159657284",
    body = "Hello from Python!"
)
print(message.sid)
