from typing import Union
from smtplib import SMTPException

from .services import send_mails, check_users
from config.celery import app


@app.task
def send(id_course: int,
         body_subject: str='courses/send_mail_subject.txt',
         body_template: str='courses/send_mail_instance.html'
         ) -> None:
    """Задание для события и рассписания, оправка писем пользователям

    Args:
        object_unique_name (str|None): Уникальное имя обекта_
    """    
    try:
        send_mails(id_course, body_subject, body_template)
    except SMTPException as e:
        print(e)
        

@app.task
def check_non_active_users():
    """Проверка не активных пользователей
    """    
    return check_users()
