import asyncio
from urllib.parse import unquote

import aiohttp
from flask import current_app


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
UPLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
YANDEX_DISK_PATH_PREFIX = '/'


def is_yandex_disk_path(path):
    return (
        isinstance(path, str)
        and path.startswith(YANDEX_DISK_PATH_PREFIX)
    )


def get_auth_headers():
    return {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}'
    }


async def get_download_link(path, session=None):
    owns_session = session is None
    if owns_session:
        session = aiohttp.ClientSession()
    try:
        async with session.get(
            DOWNLOAD_LINK_URL,
            headers=get_auth_headers(),
            params={'path': path, 'fields': 'href'},
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data['href']
    finally:
        if owns_session:
            await session.close()


async def upload_file(session, file_storage):
    disk_path = 'app:/' + file_storage.filename
    async with session.get(
        UPLOAD_LINK_URL,
        headers=get_auth_headers(),
        params={
            'path': disk_path,
            'overwrite': 'true',
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        upload_url = (await response.json())['href']

    async with session.put(
        upload_url,
        data=file_storage.read(),
    ) as response:
        response.raise_for_status()
        location = response.headers['Location']

    decoded_location = unquote(location)
    stored_path = decoded_location.removeprefix('/disk')
    await get_download_link(stored_path, session)
    return file_storage.filename, stored_path


async def upload_files(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(
            upload_file(session, file_storage)
            for file_storage in files
        ))
