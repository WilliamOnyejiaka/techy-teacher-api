from src.api.v1.models.videos import Video
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.api.v1.models import db
from flask import Blueprint, jsonify
from src.api.v1.models.bookmarks import Bookmark, bookmark_schema
from src.api.v1.models.videos import video_schema, Video
from flask_jwt_extended import jwt_required, get_jwt_identity

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.post("/<int:id>")
@jwt_required()
def add_video_bookmark(id):
    user_id = get_jwt_identity()
    video = Video.query.filter_by(id=id).first()

    if video:
        if Bookmark.query.filter_by(video_id=id).first():
            return jsonify({'message': f'bookmark with the id {id} already exits'})

        bookmark = Bookmark(user_id, id)
        bookmark.create()
        return bookmark_schema.jsonify(bookmark), HTTP_201_CREATED
    return jsonify({'error': f'video with the id {id} not found'}), HTTP_404_NOT_FOUND


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmarked_video(id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=id, user_id=user_id).first()

    if bookmark:
        video = Video.query.filter_by(
            id=bookmark.video_id).first()
        return video_schema.jsonify(video), HTTP_200_OK
    return jsonify({'error': f'bookmark with the id {id} not found'}), HTTP_404_NOT_FOUND


@bookmarks.get("/")
@jwt_required()
def get_bookmarked_videos():
    user_id = get_jwt_identity()
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    video_ids = []
    data = []

    for bookmark in bookmarks:
        video_ids.append(bookmark.video_id)

    for video_id in video_ids:
        video = Video.query.filter_by(id=video_id).first()
        if video:
            data.append({
                'id': video.id,
                'video_url': video.video_url,
                'image_url': video.image_url,
                'title': video.title,
                'description': video.description,
                'created_at': video.created_at,
                'updated_at': video.updated_at,
            })
    return jsonify({'data': data}), HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(id=id, user_id=user_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT
    return jsonify({'error': f'bookmark with the id {id} not found'}), HTTP_404_NOT_FOUND
