import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app, db
from yacut.api_errors import InvalidAPIUsage
from yacut.constants import (
    DUPLICATED_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
    MAX_CUSTOM_ID_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_PATTERN,
)
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


def is_valid_custom_id(custom_id):
    return (
        isinstance(custom_id, str)
        and len(custom_id) <= MAX_CUSTOM_ID_LENGTH
        and re.fullmatch(SHORT_ID_PATTERN, custom_id) is not None
    )


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not isinstance(data, dict) or 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if not is_valid_custom_id(custom_id):
            raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
        if (
            custom_id in RESERVED_SHORT_IDS
            or URLMap.query.filter_by(short=custom_id).first() is not None
        ):
            raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap(original=data['url'], short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True,
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND,
        )
    return jsonify({'url': url_map.original})
