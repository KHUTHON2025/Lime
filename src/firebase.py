import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

service_key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred)

#FCM example code
registration_token = 'PHONE_TOKEN'
print(registration_token)

# See documentation on defining a message payload.
message = messaging.Message(
    data={
        'score': '850',
        'time': '2:45',
    },
    token=registration_token,
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)
