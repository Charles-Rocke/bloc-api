from fastapi import FastAPI

def create_app():
		app = FastAPI()
		# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
		
		from sql_app import database
		
	
		# from .views import views
		# from .auth import auth
		# from .util import util
		# from .admin import admin

		# app.register_blueprint(views,url_prefix='/')
		# app.register_blueprint(auth,url_prefix='/')
		# app.register_blueprint(util,url_prefix='/')
		# app.register_blueprint(admin,url_prefix='/admin')

		from sql_app.models import User, WebAuthnCredential, EndUser, EndUserWebAuthnCredential

		#create_database(app)

		# login_manager = LoginManager()
		# login_manager.login_view = 'auth.login'
		# login_manager.init_app(app)

		# @login_manager.user_loader
		# def load_user(id):
		# 		return User.query.get(int(id))

		
			
		return app