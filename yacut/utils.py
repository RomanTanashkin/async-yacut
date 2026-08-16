from random import choices

from yacut.constants import (
    AUTO_SHORT_ID_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_CHARACTERS,
)
from yacut.models import URLMap


def get_unique_short_id(length=AUTO_SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(choices(SHORT_ID_CHARACTERS, k=length))
        if (
            short_id not in RESERVED_SHORT_IDS
            and URLMap.query.filter_by(short=short_id).first() is None
        ):
            return short_id
