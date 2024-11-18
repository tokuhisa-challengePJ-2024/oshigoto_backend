import os
from django.core.wsgi import get_wsgi_application
import firebase_admin
from firebase_admin import credentials

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Firebase 初期化
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
FIREBASE_CREDENTIALS_PATH = '/Users/tokuhisaryuunosuke/grad_product/oshigotoApi/firebase/credentials.json'

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

application = get_wsgi_application()
