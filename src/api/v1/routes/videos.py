from src.api.v1.models.videos import Video
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.api.v1.models import db
from flask import request, Blueprint, jsonify
from src.api.v1.models.videos import Video, video_schema, videos_schema
from flask_jwt_extended import jwt_required
import validators

videos = Blueprint("videos", __name__, url_prefix="/api/v1/videos")


@videos.post("/")
@jwt_required()
def add_video():
    video_url = request.get_json().get('video_url', None)
    image_url = request.get_json().get('image_url', None)
    title = request.get_json().get('title', None)
    description = request.get_json().get('description', None)

    if not validators.url(video_url):
        return jsonify({'error': 'enter a valid url'}), HTTP_400_BAD_REQUEST

    if not validators.url(image_url):
        return jsonify({'error': 'enter a valid url'}), HTTP_400_BAD_REQUEST

    if not title:
        return jsonify({'error': 'title can not be empty'}), HTTP_400_BAD_REQUEST

    if not description:
        return jsonify({'error': 'description can not be empty'}), HTTP_400_BAD_REQUEST

    if Video.query.filter_by(video_url=video_url).first():
        return jsonify({'error': 'video url already exits'}), HTTP_409_CONFLICT

    if Video.query.filter_by(image_url=image_url).first():
        return jsonify({'error': 'image url already exits'}), HTTP_409_CONFLICT

    if Video.query.filter_by(title=title).first():
        return jsonify({'error': 'title already exits'}), HTTP_409_CONFLICT

    video = Video(video_url, image_url, title, description)
    video.create()

    return video_schema.jsonify(video), HTTP_201_CREATED


@videos.get("/<int:id>")
@jwt_required()
def get_video(id):
    video = Video.query.filter_by(
        id=id).first()
    if video:
        return video_schema.jsonify(video), HTTP_200_OK
    return jsonify({'error': f'video with the id {id} not found'}), HTTP_404_NOT_FOUND


@videos.get("/")
@jwt_required()
def get_videos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    videos = Video.query.filter(Video.id > 0).paginate(
        page=page, per_page=per_page)
    data = []

    for video in videos.items:
        data.append({
            'id': video.id,
            'video_url': video.video_url,
            'image_url': video.image_url,
            'title': video.title,
            'description': video.description,
            'created_at': video.created_at,
            'updated_at': video.updated_at,
        })

    meta = {
        'page': videos.page,
        'pages': videos.pages,
        'total_count': videos.total,
        'prev_page': videos.prev_num,
        'next_page': videos.next_num,
        'has_next': videos.has_next,
        'has_prev': videos.has_prev,
    }
    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


@videos.patch("/title/<int:id>")
@jwt_required()
def update_video_title(id):
    video = Video.query.filter_by(
        id=id).first()
    if video:
        title = request.get_json().get('title')
        if Video.query.filter_by(title=title).first():
            return jsonify({'error': f'video with the title {title} already exists'}), HTTP_409_CONFLICT

        video.title = title
        db.session.commit()
        return video_schema.jsonify(video), HTTP_200_OK
    return jsonify({'error': f'video with the id -{id} not found'}), HTTP_404_NOT_FOUND


@videos.patch("/description/<int:id>")
@jwt_required()
def update_video_description(id):
    video = Video.query.filter_by(
        id=id).first()
    if video:
        description = request.get_json().get('description', video.description)

        video.description = description
        db.session.commit()
        return video_schema.jsonify(video), HTTP_200_OK
    return jsonify({'error': f'video with the id -{id} not found'}), HTTP_404_NOT_FOUND


@videos.delete("/<int:id>")
@jwt_required()
def delete_video(id):
    video = Video.query.filter_by(
        id=id).first()
    if video:
        db.session.delete(video)
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT
    return jsonify({'error': f'video with the id {id} not found'}), HTTP_404_NOT_FOUND


@videos.get("/search")
@jwt_required()
def search():
    keyword = request.args.get('q', '')
    results = Video.query.filter(Video.id > 0).msearch(
        keyword).all()
    data = videos_schema.dump(results)

    return jsonify({'data': data})
