# Pythonの公式イメージをベースにする
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY backend/requirements.txt /app/

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクト全体をコピー
COPY backend/ /app/

# ファイルの存在確認コマンドを追加
RUN ls -al /app

# 作業ディレクトリを`/app`から`/app/backend`に変更
WORKDIR /app

# Django開発サーバーを起動するコマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
