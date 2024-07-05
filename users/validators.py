from typing import Any, List, Union, Callable

from rest_framework.serializers import ValidationError
from django.contrib.auth.password_validation import get_default_password_validators


class ValidatorSetPasswordUser:
    
    def __init__(self, passwords: List[str]) -> None:
        if not isinstance(passwords, list):
            raise TypeError('Поле "fields" должно было List')
        if len(passwords) != 2:
            raise KeyError('Неоходимо указать два пароля для сравнения')
        for password in passwords:
             if not isinstance(password, str):
                raise TypeError('Аргумент "password" может быть только строкой')
        self.passwords = passwords
        
    def _validate_password(self, password):
        errors = []
        password_validators = get_default_password_validators()
        for validator in password_validators:
            try:
                validator.validate(password)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)
    
    def _check_validate_password(self, password: str) -> Union[ValidationError, None]:
        self._validate_password(password)
        
    def _check_some_passwords(self, passwords: List[str]) -> Union[ValidationError, None]:
        password, password_check = passwords
        if password and password_check and password != password_check:
            raise ValidationError(
                'Пароли не совпадают'
            )
            
    def __call__(self, attrs: Any) -> Callable:
        checked_values = [
                value for password, value in attrs.items() if password in self.passwords
            ]
        self._check_some_passwords(checked_values)
        self._check_validate_password(checked_values[0])
        
        
class ValidatorOneValueInput:
    
    def __init__(self, fields: List[str]) -> None:
        if not isinstance(fields, list):
            raise TypeError('Поле "fields" должно было List')
        if len(fields) != 2:
            raise KeyError('Неоходимо указать два значения для проверки')
        for field in fields:
             if not isinstance(field, str):
                raise TypeError('Аргумент "field" может быть только строкой')
        self.fields = fields
        
    def __call__(self, attrs: Any) -> Callable:
        checked_values = [
                value for field, value in attrs.items() if field in self.fields
                and not None
            ]
        if len(checked_values) > 1:
            raise ValidationError(f'{self.fields[0]} и {self.fields[-1]} не могут быть опеределенны вместе')
        if len(checked_values) < 1:
            raise ValidationError(f'Нужно опередить одно из полей ({self.fields[0]}, {self.fields[-1]})')
