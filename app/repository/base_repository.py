from app.util.firebase import get_firestore_client


class BaseRepository:
    def __init__(self):
        self.db = get_firestore_client()
