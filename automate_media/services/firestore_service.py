import firebase_admin
from firebase_admin import credentials, firestore
import os

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

async def save_lead(lead_data):
    lead_collection = firestore_client.collection('leads')
    lead_doc = lead_collection.document(lead_data['id'])
    lead_doc.set(lead_data)
    return lead_doc.id
