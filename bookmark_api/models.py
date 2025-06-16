from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() 

class Bookmark(db.Model):
    __tablename__ = 'bookmarks' # テーブル名

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False) # URLは必須
    title = db.Column(db.String(200), nullable=True) # タイトルは任意
    description = db.Column(db.Text, nullable=True)   # 説明も任意
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # 作成日時 (自動で現在時刻が入る)

    def __repr__(self):
        return f'<Bookmark {self.id}: {self.title or self.url}>'

    # APIで返すJSON形式に変換するメソッド (任意だが便利)
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() # ISO形式の文字列に変換
        }