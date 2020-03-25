from flask import Blueprint, current_app, request
from .auth import requires_auth, moderator
from .elastic import Elasticsearch



logs = Blueprint('logs', __name__, )


@logs.route('/get_logs', methods=['POST'])
@requires_auth
@moderator
def get_logs(user):
    params = request.json
    es = Elasticsearch(current_app.config['ES_CONNECTION_STRING'], index=current_app.config['INDEX_NAME'])
    try:
        size = params.get('size', 25)
        offset = params.get('offset', 0)
        return es.get_logs(point_id=params.get('id'), size=size, offset=offset)
    except AttributeError:
        return es.get_logs()
