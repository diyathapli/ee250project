from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'AC1ae904bb7ab7a6b87f6587b712b45657' # replace with your Account SID
TWILIO_AUTH_TOKEN = 'cd080981ea88a3291fdbcf2cf762c511' # replace with your Auth Token
TWILIO_PHONE_SENDER = "7853845784" # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = "7074943499" # replace with your phone number

def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body="Knocking sequence failed! Beware of potential intruders.")
    print(message.sid)
    
    
