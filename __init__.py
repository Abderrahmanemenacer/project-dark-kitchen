from datetime import timedelta
import cloudinary
from flask import Flask
from extensions import db, jwt, mail , oauth , bcrypt ,cors
from dotenv import load_dotenv
import os



def create_app():
    load_dotenv()
    app = Flask(__name__)

    # ✅ CORS Configuration
    cors.init_app(app, 
        origins=["*"],
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization', 'X-CSRF-TOKEN'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )

    # ✅ Basic Flask Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL_LOCALHOST")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # ✅ JWT Configuration for localStorage
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1296000
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    
    # Configure JWT to use headers instead of cookies
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Changed from 'cookies' to 'headers'
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'  # This will expect "Bearer <token>" in headers
    
    # Disable all cookie-related configurations since we're using localStorage
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_HTTPONLY'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # Mail configuration
    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    )

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    # Import Auth module
    from AUTHService import Auth
    Auth.init_serializer(app.config['SECRET_KEY'])

    from routes import routes
    app.register_blueprint(routes)

    # Cloudinary config
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    return app
