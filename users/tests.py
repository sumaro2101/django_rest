from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from courses.models import Course, Lesson
from users.models import Payments
from users.validators import ValidatorOneValueInput, ValidatorSetPasswordUser


# ===============================UserTests===============================
class TestUserApi(APITestCase):
    
    def test_view_user(self):
        """Тест вывода пользователя
        """        
        user = get_user_model().objects.create(username='test', email='test@gmail.com', password='testroot')
        self.client.force_authenticate(user=user)
        url = reverse('users:user_view', kwargs={'pk': user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'username': 'test',
                                         'first_name': '',
                                         'last_name': '',
                                         'email': 'test@gmail.com',
                                         'is_staff': False,
                                         'is_active': True,
                                         'phone': None,
                                         'city': None,
                                         'avatar': None,
                                         'payments_info': []
                                         })
    
    def test_create_user(self):
        """Тест создания пользователя
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'password': 'testroot',
                'password_check': 'testroot',
                }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, 'test')
        
    def test_create_user_bad_arguments(self):
        """Тест создания пользователя с недостающими аргументами
        """
        url = reverse('users:user_create')
        data = {'email': 'test@gmail.com',
                'password': 'testroot',
                }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)
        
    def test_create_validate_password(self):
        """Тест валидации не одинаковых паролей
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'password': 'testroot',
                'password_check': 'testrootnotsome',
                }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [ErrorDetail(string='Пароли не совпадают', code='invalid')]})
        
    def test_create_validate_common_password(self):
        """Тест валидации простого пароля
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'password': '12345678',
                'password_check': '12345678',
                }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [ErrorDetail(string='Введённый пароль слишком широко распространён.', code='password_too_common')]})
        
    def test_update_user(self):
        """Тест изменения пользователя
        """        
        user = get_user_model().objects.create(username='test', email='test@gmail.com', password='testroot')
        self.client.force_authenticate(user=user)
        
        url = reverse('users:user_update_delete', kwargs={'pk': user.pk})
        data = {'username': 'change',
                'email': 'change@gmail.com',
                }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(get_user_model().objects.filter(username='change').exists())
        self.assertFalse(get_user_model().objects.filter(username='test').exists())
        
    def test_change_activity_user(self):
        """Тест изменения активности пользователя 
        """
        user = get_user_model().objects.create(username='test', email='test@gmail.com', password='testroot')
        self.client.force_authenticate(user=user)
        url = reverse('users:user_update_delete', kwargs={'pk': user.pk})
        
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertFalse(get_user_model().objects.get(username='test').is_active)
        
    def test_validator_set_password_user(self):
        """Проверка валидатора для пользователя
        """
        # Проверка на число    
        with self.assertRaises(TypeError):
            ValidatorSetPasswordUser(223)
        
        # Проверка на список с числом  
        with self.assertRaises(TypeError):
            ValidatorSetPasswordUser(['str', 223])
            
        # Проверка списка < 2
        with self.assertRaises(KeyError):
            ValidatorSetPasswordUser(['str',])
            
        # Проверка списка > 2
        with self.assertRaises(KeyError):
            ValidatorSetPasswordUser(['str', 'str', 'str'])

        validate = ValidatorSetPasswordUser(['first', 'second'])
        # Проверка корректности заполнения
        self.assertEqual(validate.passwords, ['first', 'second'])
        # Проверка корректности проверки правильных аргументов
        self.assertIsNone(validate({'first': 'rootpassword', 'second': 'rootpassword'}))   

        
# ===============================PaymentTests===============================
class TestApiPayments(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create(username='test', email='test@gmail.com', password='testroot')
        self.course = Course.objects.create(course_name='course', description='description_of_course')
        self.lesson = Lesson.objects.create(course=self.course, lesson_name='lesson', description='description_of_lesson')
        self.client.force_authenticate(user=self.user)
        
    def test_view_payments(self):
        """Тест вывода платежей
        """        
        Payments.objects.create(user=self.user, pay_course=self.course, payment_amount=32000.00, payment_method='cash')
        url = reverse('users:payments_list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 1,
                                         'next': None,
                                         'previous': None,
                                         'results': [{'user': self.user.pk,
                                                      'date_of_pay': response.data['results'][0]['date_of_pay'],
                                                      'pay_course': self.course.pk,
                                                      'pay_lesson': None,
                                                      'payment_amount': '32000.00',
                                                      'payment_method': 'cash'}]})
        
    def test_payments_detail_user(self):
        """Тест вывода платежей в информации о пользователе
        """
        Payments.objects.create(user=self.user, pay_course=self.course, payment_amount=32000.00, payment_method='cash')
        url = reverse('users:user_view', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payments_info'], [{'user': self.user.pk,
                                                      'date_of_pay': response.data['payments_info'][0]['date_of_pay'],
                                                      'pay_course': self.course.pk,
                                                      'pay_lesson': None,
                                                      'payment_amount': '32000.00',
                                                      'payment_method': 'cash'}])
        
    def test_create_course_payments(self):
        """Тест создания платежа для курса
        """        
        url = reverse('users:payments_list')
        data = {
            'user': self.user.pk,
            'pay_course': self.course.pk,
            'payment_amount': 10000.00,
            'payment_method': 'money_transfer'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payments.objects.count(), 1)
        self.assertEqual(Payments.objects.get().payment_amount, 10000.00)
        
    def test_create_lesson_payments(self):
        """Тест создания платежа для урока
        """        
        url = reverse('users:payments_list')
        data = {
            'user': self.user.pk,
            'pay_lesson': self.lesson.pk,
            'payment_amount': 3000.00,
            'payment_method': 'cash'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payments.objects.count(), 1)
        self.assertEqual(Payments.objects.get(~Q(pay_lesson=None)).payment_amount, 3000.00)
        
    def test_validate_course_lesson_together(self):
        """Тест валидации курса и урока вместе
        """        
        url = reverse('users:payments_list')
        data = {
            'user': self.user.pk,
            'pay_course': self.course.pk,
            'pay_lesson': self.lesson.pk,
            'payment_amount': 12000.00,
            'payment_method': 'cash'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [ErrorDetail(string='pay_course и pay_lesson не могут быть опеределенны вместе', code='invalid')]})
        
    def test_validate_course_lesson_empty(self):
        """Тест валидации без курса и урока
        """        
        url = reverse('users:payments_list')
        data = {
            'user': self.user.pk,
            'payment_amount': 12000.00,
            'payment_method': 'cash'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [ErrorDetail(string='Нужно опередить одно из полей (pay_course, pay_lesson)', code='invalid')]})
        
    def test_validator_one_value_input(self):
        """Проверка валидатора платежей
        """
        # Проверка на число    
        with self.assertRaises(TypeError):
            ValidatorOneValueInput(223)
        
        # Проверка на список с числом  
        with self.assertRaises(TypeError):
            ValidatorOneValueInput(['str', 223])
            
        # Проверка списка < 2
        with self.assertRaises(KeyError):
            ValidatorOneValueInput(['str',])
            
        # Проверка списка > 2
        with self.assertRaises(KeyError):
            ValidatorOneValueInput(['str', 'str', 'str'])

        validate = ValidatorOneValueInput(['first', 'second'])
        # Проверка корректности заполнения
        self.assertEqual(validate.fields, ['first', 'second'])
        # Проверка корректности проверки правильных аргументов
        self.assertIsNone(validate({'second': 1}))
        