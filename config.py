class Config(object):
    SECRET_KEY = 'test-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ACM_member.db'
    SQLALCHEMY_BINDS={"BLocklist":'sqlite:///Blocklist.db'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "secret" 
    JWT_TOKEN_LOCATION = ["headers"]