from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()


# Extensions initialization
bcrypt = Bcrypt()
mail = Mail()
oauth = OAuth()
cors = CORS()