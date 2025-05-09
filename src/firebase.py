import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
from firebase_admin import messaging

load_dotenv()

service_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

cred = credentials.Certificate(service_key_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized successfully.")
else:
    print("ℹ️ Firebase already initialized.")

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
