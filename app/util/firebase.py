import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FIREBASE_KEY = BASE_DIR / "creds" / "resume-generator-firebase.json"


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY)
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    init_firebase()
    return firestore.client()