import os

# プロジェクトのベースディレクトリ
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bookmarks.db') # bookmarks.dbというファイルに保存
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    

