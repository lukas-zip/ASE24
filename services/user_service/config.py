import os

# set testing to false
TESTING = False
# get base direction
basedir = os.path.abspath(os.path.dirname(__file__))
#get db file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'persistent/user.db')
# set sql settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
# set wtf settings
WTF_CSRF_ENABLED = True
# set secret key
SECRET_KEY = 'a-very-secret-secret'