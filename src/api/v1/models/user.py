from src.api.v1.models import bookmarks
from . import db,serializer
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model):

	__tablename__ = 'user'

	id = db.Column(db.Integer,nullable=False,primary_key=True)
	first_name = db.Column(db.String(50),nullable=False)
	last_name =	db.Column(db.String(50),nullable=False)
	email = db.Column(db.String,unique=True,nullable=False)
	password = db.Column(db.Text,nullable=False)
	bookmarks = db.relationship("Bookmark",backref="user",lazy="dynamic",cascade="all, delete ,delete-orphan")
	created_at = db.Column(db.DateTime,default=datetime.now())
	updated_at = db.Column(db.DateTime,onupdate=datetime.now())

	def __init__(self,first_name,last_name,email,password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = generate_password_hash(password)

	def create(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return f'User>>>{self.first_name} {self.last_name}'


class UserSchema(serializer.Schema):
	class Meta:
		fields = ('id', 'first_name', 'last_name',
		          'email', 'created_at', 'updated_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)



