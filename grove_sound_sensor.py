#!/usr/bin/env python
#
# GrovePi Example for using the Grove Sound Sensor and the Grove LED
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Modules:
#	 http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
#	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import time
import grovepi
from twilio.rest import Client


#Send an SMS message to the client's phone number through the number registered with twilio
TWILIO_ACCOUNT_SID = 'AC1ae904bb7ab7a6b87f6587b712b45657' # replace with your Account SID
TWILIO_AUTH_TOKEN = 'cd080981ea88a3291fdbcf2cf762c511' # replace with your Auth Token
TWILIO_PHONE_SENDER = '+17853845784' # replace with the phone number you registered in twilio
TWILIO_PHONE_RECIPIENT = '+17074943499' # replace with your phone number

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0

buzzer = 2
button = 4

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(buzzer,"OUTPUT")

WINDOW_SIZE = 15
THRESHOLD = 100
LONG_LENGTH = 60
SHORT_LENGTH = 20
num_high = 0;
raw_data = []
averaged_data = []
num_points = 0

# Values stored in array: 0 - Dot | 1 - Dash
# Morse Code: USC (U: Dot, Dot, Dash | S: Dot, Dot, Dot | C: Dash, Dot, Dash, Dot)
expected_code = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
code_index = 0

def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=TWILIO_PHONE_RECIPIENT,
        from_=TWILIO_PHONE_SENDER,
        body=alert_str)
    print(message.sid)
'''
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
		to=TWILIO_PHONE_RECIPIENT,
		from_=TWILIO_PHONE_SENDER,
		body='Knocking sequence failed! Beware of potential intruders.')
print(message.sid)
'''

while True:
    try:
        button_val = grovepi.digitalRead(button)

        if button_val:
            grovepi.digitalWrite(buzzer, 1)

        else:
            grovepi.digitalWrite(buzzer, 0)


        # Code Entered Condition
        if code_index == 10:
            code_index = 0
            send_text_alert('Code Entered! Welcome In!')

        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)
        raw_data.append(sensor_value)
        num_points = num_points + 1

        if num_points >= WINDOW_SIZE:
            window = raw_data[num_points - WINDOW_SIZE : num_points]
            window_averaged = round(sum(window) / WINDOW_SIZE)
            if window_averaged > THRESHOLD:
                num_high = num_high + 1
            else:
                if num_high < LONG_LENGTH and num_high > SHORT_LENGTH:
                    print("Short BUTTON")
                    if(expected_code[code_index] == 0):
                        code_index = code_index + 1
                    else:
                        code_index = 0
                        send_text_alert('Knocking sequence failed! Beware of potential intruders.')
                if num_high > LONG_LENGTH:
                    print("LONG BUTTON")
                    if(expected_code[code_index] == 1):
                        code_index = code_index + 1
                    else:
                        code_index = 1
                        send_text_alert('Knocking sequence failed! Beware of potential intruders.')
                num_high = 0
            averaged_data.append(window_averaged)
            print("sensor_value = %d" %window_averaged)
            
        time.sleep(.01)

    except IOError:
        print ("Error")
        
