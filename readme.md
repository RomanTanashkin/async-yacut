# YaCut

YaCut — Flask-сервис для создания коротких ссылок и асинхронной загрузки
нескольких файлов на Яндекс Диск.

## Запуск в Windows

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/RomanTanashkin/async-yacut.git
cd async-yacut
```

Создайте и активируйте виртуальное окружение в Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

Установите зависимости:

```bash
python -m pip install -r requirements.txt
```

Создайте в корне проекта файл `.env`:

```text
FLASK_APP=yacut
SECRET_KEY=replace-with-a-secret-key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your-yandex-disk-oauth-token
```

Создайте таблицы базы данных:

```bash
flask shell
```

В интерактивной консоли выполните:

```python
from yacut import db
db.create_all()
exit()
```

Запустите приложение:

```bash
flask run
```

## Проверка

```bash
pytest
flake8 yacut config.py
```

API предоставляет два эндпоинта:

- `POST /api/id/` — создать короткую ссылку;
- `GET /api/id/<short_id>/` — получить исходную ссылку.
