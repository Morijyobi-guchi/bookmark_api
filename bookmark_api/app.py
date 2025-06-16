from flask import Flask, request, jsonify
from models import db, Bookmark # models.py から db と Bookmark をインポート
from config import Config     # config.py から Config をインポート
# from flask_migrate import Migrate # もしFlask-Migrateを使う場合
from flask_cors import CORS # クロスオリジンリソースシェアリングを有効にするため

app = Flask(__name__)
app.config.from_object(Config) # 設定を読み込み
CORS(app) # CORSを有効にする

db.init_app(app) # FlaskアプリとSQLAlchemyを連携
# migrate = Migrate(app, db) # もしFlask-Migrateを使う場合

# データベーステーブルの作成 (初回実行時やモデル変更時に必要)
# 開発中は、Pythonインタプリタで以下のコマンドを実行してテーブルを作成します。
# from app import app, db
with app.app_context():
    db.create_all()
# (Flask-Migrateを使う場合は、マイグレーションコマンドで管理します)

# --- APIエンドポイント ---

# ブックマークの新規作成 (POST /api/bookmarks)
@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.get_json() # リクエストボディ (JSON) を取得
    if not data or not data.get('url'):
        return jsonify({'error': 'URL is required'}), 400

    new_bookmark = Bookmark(
        url=data['url'],
        title=data.get('title'),
        description=data.get('description')
    )
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify(new_bookmark.to_dict()), 201 # 作成されたリソースとステータスコード201を返す

# ブックマークの一覧取得 (GET /api/bookmarks)
@app.route('/api/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    return jsonify([bookmark.to_dict() for bookmark in bookmarks]), 200

# 個別ブックマークの取得 (GET /api/bookmarks/<id>)
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['GET'])
def get_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id) # 見つからなければ404エラー
    return jsonify(bookmark.to_dict()), 200

# ブックマークの更新 (PUT /api/bookmarks/<id>)
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['PUT'])
def update_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    data = request.get_json()

    bookmark.url = data.get('url', bookmark.url) # リクエストにあれば更新、なければ元の値
    bookmark.title = data.get('title', bookmark.title)
    bookmark.description = data.get('description', bookmark.description)

    db.session.commit()
    return jsonify(bookmark.to_dict()), 200

# ブックマークの削除 (DELETE /api/bookmarks/<id>)
@app.route('/api/bookmarks/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    db.session.delete(bookmark)
    db.session.commit()
    return '', 204 # コンテンツなし、成功を示すステータスコード204

if __name__ == '__main__':
    # 開発中は以下のコマンドでテーブルを作成してからアプリを起動すると良いです。
    with app.app_context():
        db.create_all() # データベースとテーブルがなければ作成
    app.run(debug=True) # 開発用サーバーを起動 (debug=Trueは開発時のみ)