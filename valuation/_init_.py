import os
from datetime import timedelta

from flask import Flask, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# flask-loginとflaskアプリケーションをつなぐ処理
login_manager = LoginManager()
# ログインする際に実行される処理 'アプリケーション名.login'
login_manager.login_view = 'app.login'
# ログイン画面にリダイレクトされた際に表示されるメッセージ
login_manager.login_message = 'ログインしてください'

app = Flask(__name__)
app.config.from_object('valuation.config')
app.secret_key = 'fugafugahogehoge'
app.permanent_session_lifetime = timedelta(minutes=1440)

db = SQLAlchemy(app)

login_manager.init_app(app)

from valuation.models import model

import valuation.views