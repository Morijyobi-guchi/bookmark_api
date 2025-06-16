# 1. ベースとなるPythonイメージを指定
FROM python:3.13-slim

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. 必要なライブラリをインストール
COPY requirements.txt .
# gunicornは本番環境でFlaskアプリを動かすための推奨サーバーです
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 4. プロジェクトのファイルをコピー
COPY . .

# 5. アプリケーションを実行するコマンドを指定
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]