from flask import flash, redirect, render_template, url_for

from yacut import app, db
from yacut.constants import (
    DUPLICATED_SHORT_ID_MESSAGE,
    RESERVED_SHORT_IDS,
)
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import get_download_link, upload_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_link = None
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if (
            custom_id in RESERVED_SHORT_IDS
            or URLMap.query.filter_by(short=custom_id).first() is not None
        ):
            flash(DUPLICATED_SHORT_ID_MESSAGE)
            return render_template('index.html', form=form)
        short_id = custom_id or get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True,
        )
    return render_template(
        'index.html',
        form=form,
        short_link=short_link,
    )


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileUploadForm()
    uploaded_files = []
    if form.validate_on_submit():
        disk_files = await upload_files(form.files.data)
        for filename, disk_path in disk_files:
            url_map = URLMap(
                original=disk_path,
                short=get_unique_short_id(),
            )
            db.session.add(url_map)
            uploaded_files.append({
                'filename': filename,
                'short_link': url_for(
                    'redirect_view',
                    short_id=url_map.short,
                    _external=True,
                ),
            })
        db.session.commit()
    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@app.route('/<string:short_id>')
async def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    if url_map.original.startswith(('http://', 'https://')):
        return redirect(url_map.original)
    return redirect(await get_download_link(url_map.original))
