import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "f89d1c36a61bb4b82bfc62143e6bda07ce7f020fd79b083f92eaf1b28dff14f5"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'password_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False