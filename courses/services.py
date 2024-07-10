from django.template import TemplateDoesNotExist
from django.urls import NoReverseMatch
from django.db.models import Q
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from smtplib import SMTPException

from typing import List

from datetime import timedelta

from courses.models import Course


def send_mails(id_object: int,
               body_subject: str,
               body_template: str
               ) -> None:
    """Отправка письма пользователям

    Args:
        id_object (int): Id целевого объекта
        body_subject (str): txt шаблон для заголовка
        body_template (str): html шаблон для тела
    """    
    try:
        course = Course.objects.get(pk=id_object)
    except:
        raise SMTPException(f'По данному ID: {id_object} курса найдено не было')
    
    subscribers = course.subscribe.all().select_related('user')
    subscribers_email = [subscribe.user.email for subscribe in subscribers]
    
    template_body = body_template
    subject_template_body = body_subject
    server_mail: str = settings.EMAIL_HOST_USER
    users: List[str] = subscribers_email
        
    context = {
    'course': course.course_name,
    'owner': course.owner,
    'id_course': id_object
    }

    #Попытка рендера заголовка с контекстом
    try:
        subject = loader.render_to_string(subject_template_body, context=context)
        subject = "".join(subject.splitlines())
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(f'По заданному пути: {subject_template_body} - шаблон не был найден')
    except NoReverseMatch:
        raise NoReverseMatch('Ошибка при постоении пути')
    
    #Попытка рендера тела с контекстом  
    try:
        body = loader.render_to_string(template_body, context=context)
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(f'По заданному пути: {template_body} - шаблон не был найден')
    except NoReverseMatch:
        raise NoReverseMatch('Ошибка при постоении пути')
        
    email_message = EmailMultiAlternatives(subject, body, server_mail, users)
    email_message.send()
    

def check_users():
    """Обход всех пользователей и проверка активных пользователей 

    Returns:
        List[str] | None: Возращает список пользователей которые были перемещены
        в неактивное состояние
    """    
    time_before_one_month = timezone.now() - timedelta(days=30)
    user_is_toggle_activity = get_user_model().objects.filter(~Q(is_staff=True) & ~Q(is_active=False) & Q(
                                                              Q(last_login=None) & Q(date_joined__lte=time_before_one_month)|
                                                              ~Q(last_login=None) & Q(last_login__lte=time_before_one_month))
                                                              )
    if user_is_toggle_activity:
        users_non_active = []
        list_to_result = []
        for user in user_is_toggle_activity:
            user.is_active = False
            list_to_result.append(f'{user.username}: {user.email}')
            users_non_active.append(user)
            
        get_user_model().objects.bulk_update(users_non_active, fields=('is_active',))
        return list_to_result
        