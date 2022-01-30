from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_msearch import Search


db = SQLAlchemy()
serializer = Marshmallow()
search = Search(db=db)

