import os
import sys
import firebase_admin


# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# FIREBASE_CONFIG = os.environ.get("FIREBASE_CONFIG")
# cred = credentials.Certificate("C:/Users/minco/OneDrive/Desktop/vs-code-projects/bpr-backend/firebase_funcs/firebase_service_account.json")

def get_app():
    return firebase_admin.initialize_app()
