import string


AUTO_SHORT_ID_LENGTH = 6
MAX_CUSTOM_ID_LENGTH = 16
SHORT_ID_CHARACTERS = string.ascii_letters + string.digits
SHORT_ID_PATTERN = rf'^[{SHORT_ID_CHARACTERS}]+$'
RESERVED_SHORT_IDS = {'files'}

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
INVALID_URL_MESSAGE = 'Указана некорректная ссылка'
