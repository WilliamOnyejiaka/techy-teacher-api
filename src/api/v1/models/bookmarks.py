from . import db,serializer
from datetime import datetime


class Bookmark(db.Model):

	__tablename__ = 'bookmarks'
	
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
	created_at = db.Column(db.DateTime, default=datetime.now())

	def __init__(self, user_id, video_id):
		self.user_id = user_id
		self.video_id = video_id

	def __repr__(self):
		return f'Img>>>{self.name}'

	def create(self):
		db.session.add(self)
		db.session.commit()


class BookmarkSchema(serializer.Schema):
	class Meta:
		fields = ('id', 'video_id', 'user_id', 'created_at')


bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)
