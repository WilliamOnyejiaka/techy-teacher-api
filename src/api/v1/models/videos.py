from . import db, serializer
from datetime import datetime

class Video(db.Model):

	__tablename__ = 'videos'
	__searchable__ = ['title']
	id = db.Column(db.Integer, primary_key=True)
	video_url = db.Column(db.Text, nullable=False, unique=True)
	image_url = db.Column(db.Text, nullable=False, unique=True)
	title = db.Column(db.Text,unique=True,nullable=False)
	description = db.Column(db.Text,nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.now())
	updated_at = db.Column(db.DateTime, onupdate=datetime.now())
	bookmarks = db.relationship("Bookmark", backref="videos", lazy="dynamic", cascade="all, delete ,delete-orphan")

	def __init__(self, video_url, image_url, title, description):
		self.video_url = video_url
		self.image_url = image_url
		self.title = title
		self.description = description

	def __repr__(self):
		return f'Img>>>{self.title}'

	def create(self):
		db.session.add(self)
		db.session.commit()


class VideoSchema(serializer.Schema):
	class Meta:
		fields = ('id', 'video_url', 'image_url',
		          'title', 'created_at', 'updated_at', 'description')


video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)
