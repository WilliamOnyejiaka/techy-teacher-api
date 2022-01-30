from src import create_app
from src.api.v1.models import db
from src.api.v1.models.videos import Video
from src.api.v1.models.user import User
from src.api.v1.models.bookmarks import Bookmark

app = create_app()
# with app.app_context():
#     db.create_all()


