import os
from django.core.wsgi import get_wsgi_application
import firebase_admin
from firebase_admin import credentials
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# プロジェクトのルートディレクトリを取得
BASE_DIR = Path(__file__).resolve().parent.parent

# ローカルのFirebase認証ファイルを読み込む
local_path = BASE_DIR / 'firebase/credentials.json'

# Firebase初期化
if not firebase_admin._apps:  # Firebaseがすでに初期化されているか確認
    cred = credentials.Certificate(str(local_path))
    firebase_admin.initialize_app(cred)

# WSGIアプリケーションの設定
application = get_wsgi_application()
