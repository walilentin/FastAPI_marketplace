from dotenv import load_dotenv

import os
from httpx_oauth.clients.google import GoogleOAuth2

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

google_oauth_client = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)


SECRET_AUTH = os.environ.get("SECRET_AUTH")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")