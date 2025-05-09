import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

service_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

cred = credentials.Certificate(service_key_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized successfully.")
else:
    print("ℹ️ Firebase already initialized.")
