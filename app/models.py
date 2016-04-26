from google.appengine.ext import ndb
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from . import login_manager

from datetime import datetime


class Permission(ndb.Model):
	Follow = 0x01
	Comment = 0x02
	Write_Articles = 0x04
	Moderate_Comments = 0x08
	Administer = 0x80


class Role(ndb.Model):
	name = ndb.StringProperty()
	default = ndb.BooleanProperty()
	permissions = ndb.IntegerProperty()

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.Follow | Permission.Comment | Permission.Write_Articles, True),
			'Moderator': (
			Permission.Follow | Permission.Comment | Permission.Write_Articles | Permission.Moderate_Comments, False),
			'Administrator': (0xff, False)
		}
		for r in roles:
			result = Role.query(Role.name == r).fetch()
			if not result:
				result = Role(name=r)
				result.permissions = roles[r][0]
				result.default = roles[r][1]
				result.put()


class DatastoreAvator(ndb.Model):
	data = ndb.BlobProperty(default=None)
	filename = ndb.StringProperty()
	minetype = ndb.StringProperty()
	avator_link = ndb.StringProperty()

	user_email = ndb.StringProperty()


class DatastoreFile(ndb.Model):
	time_stamp = ndb.DateTimeProperty(default=datetime.utcnow())
	image = ndb.BlobProperty(default=None)
	imagename = ndb.StringProperty()
	minetype = ndb.StringProperty()

	itemName = ndb.StringProperty()
	estimateValue = ndb.StringProperty()
	description = ndb.TextProperty()
	image_link = ndb.StringProperty()
	category = ndb.StringProperty()
	eOrd = ndb.StringProperty()

	haveExchange = ndb.BooleanProperty(default=False)

	user_email = ndb.StringProperty()
	user_name = ndb.StringProperty()
	user_avator_link = ndb.StringProperty()


class PostText(ndb.Model):
	textBody = ndb.TextProperty()
	time_stamp = ndb.DateTimeProperty(default=datetime.utcnow())
	author_email = ndb.StringProperty()
	author_name = ndb.StringProperty()
	author_avator_link = ndb.StringProperty()
	post_for_item = ndb.StringProperty()


# class Followee(ndb.Model):
# 	name = ndb.StringProperty()


# class Follower(ndb.Model):
# 	name = ndb.StringProperty()


class User(ndb.Model, UserMixin):
	name = ndb.StringProperty()
	password_hash = ndb.StringProperty()
	email = ndb.StringProperty()
	phone = ndb.StringProperty()
	isConfirmed = ndb.BooleanProperty()

	location = ndb.StringProperty()
	about_me = ndb.TextProperty()
	member_since = ndb.DateTimeProperty(default=datetime.utcnow())
	last_seen = ndb.DateTimeProperty(default=datetime.utcnow())

	role = ndb.StructuredProperty(Role)
	postTexts = ndb.StructuredProperty(PostText, repeated=True)
	postItem = ndb.StructuredProperty(DatastoreFile, repeated=True)
	avator = ndb.StructuredProperty(DatastoreAvator)
	avator_link = ndb.StringProperty()

	# followee = ndb.StructuredProperty(Followee, repeated = True)
	# follower = ndb.StructuredProperty(Follower, repeated = True)

	# confirm_key = ndb.IntegerProperty()

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		Role.insert_roles()
		if self.role is None:
			if self.email == current_app.config['FLASKY_ADMIN']:
				self.role = Role.query(Role.permissions == 0xff).fetch()[0]
			if self.role is None:
				self.role = Role.query(Role.default == True).fetch()[0]

	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.Administer)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer('hard to guss string', expiration)
		return s.dumps({'confirm': self.email})

	def confirm(self, token):
		s = Serializer('hard to guss string')
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.email:
			return False
		self.isConfirmed = True
		self.put()
		return True

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.email)

	def __repr__(self):
		return '<User %r>' % (self.email)

	def ping(self):
		self.last_seen = datetime.utcnow()
		self.put()


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(email):
	return User.query(User.email == email).fetch()[0]
