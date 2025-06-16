# 1. ベースとなるNode.jsイメージを指定
FROM node:20-alpine

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. 依存ライブラリをインストール
COPY package*.json ./
RUN npm install

# 4. プロジェクトのファイルをコピー
COPY . .

# 5. Vite開発サーバーを起動するコマンド
CMD ["npm", "run", "dev", "--", "--host"]