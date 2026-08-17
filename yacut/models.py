from datetime import datetime

from yacut import db
from yacut.constants import MAX_CUSTOM_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
