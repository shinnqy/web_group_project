import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	CSRF_ENABLED = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guss string'
	# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[CUHK Exchange]'
	FLASKY_MAIL_SENDER = 'CUHK Exchange Admin <Admin@cuhkexchange.com>'
	FLASKY_ADMIN = '1155065988@link.cuhk.edu.hk'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	# MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'shinn--qy@163.com'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'qy1991102691'
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	
class TestingConfig(Config):
	TESTING = True
	# SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	TESTING = True
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    