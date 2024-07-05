import re
from typing import Union

YOUTUBE_REGEX = re.compile(r'(^((w{3}\.{1}){0,1})youtube((\.+(com)){0,1})$)|(^youtu\.be$)')

def check_youtube_string(value: str) -> Union[re.Match, None]:
    """Проверяет с помощью регулярного выражение является ли ссылка youtube

    Args:
        value (str): Значение которое нужно проверить

    Returns:
        Union[re.Match, None]: Возвращается результат проверки
    """    
    if isinstance(value, str):
        return YOUTUBE_REGEX.match(value)
