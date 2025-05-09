import os
import firebase_admin
from firebase_admin import credentials

service_key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred)
