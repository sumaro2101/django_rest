from rest_framework.validators import ValidationError

from courses.regexp import check_youtube_string

from typing import Any, Union, List


class ValidateOnlyYoutubeLink:

    def __init__(self, link: str) -> None:
        if not isinstance(link, str):
            raise TypeError(
                'Поле ссылки на видео может быть только str типом',
                )
        self.link = link

    def _is_youtube(self, value: List[str]) -> Union[None, ValidationError]:
        """Проверяет принадлежность ссылки к Youtube видео-хостингу

        Args:
            value (str): Значение для проверки 

        Returns:
            Union[None, ValidationError]: Возвращает None в
            случае успеха, а иначе ValidationError
        """
        link = value[-1]
        try:
            list_of_link = link.split('/')
            if list_of_link[0] in ['https:', 'http:']:
                domen = list_of_link[2]
            else:
                domen = None
        except IndexError:
            domen = None

        if domen:
            is_youtube = check_youtube_string(domen)
            if not is_youtube:
                raise ValidationError(
                    f'Ссылка "{link}", не является ссылкой '
                    'на Youtube видео-хостинг',
                    )

    def __call__(self, attrs) -> Any:
        checked_values = [
                value for link, value in attrs.items() if link in self.link
                and not None
            ]
        if checked_values:
            if not len(checked_values) == 1:
                raise ValidationError(
                    f'Было получено более одного '
                    f'значения по полю {self.link}',
                    )

            self._is_youtube(checked_values)
