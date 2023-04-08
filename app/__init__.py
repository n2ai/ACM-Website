from flask import Flask
from config import Config
from app.database import db
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect,validate_csrf
from flask_login import LoginManager


app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = False

login = LoginManager(app)

db.init_app(app)
csrf = CSRFProtect(app)
CORS(app)


from app import routes

if __name__ == "__main__":
    app.run(debug=True)