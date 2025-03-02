#ddd
import os

class Config:
   SECRET_KEY=os.environ.get('SECRET_KEY')#found using secrets.token_hex(16) in the terminal
   SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
   TEMPLATES_AUTO_RELOAD = True
   MAIL_SERVER = 'smtp.googlemail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = os.environ.get('MAIL_USERNAME') #use your mail and generated app key.
   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
