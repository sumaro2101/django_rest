from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from rest_framework.request import Request

from typing import Union, Any, Dict

import stripe

from courses.models import Course, Lesson
from users.models import Payments
from config.utils import find_env


class StripeItem:
    """Класс создания продукта
    """ 
       
    def __init__(self, product: Any) -> None:
        """Инициализация продукта
        """        
        stripe.api_key = find_env('STRIPE_API_KEY')
        self.item = self._set_object_stripe(product)
        
    def _create_product(self, product, product_name) -> stripe.Product:
        """Создание данных о продукте
        """
        product_description = product.description if product.description else 'default_description'
        created_product = stripe.Product.create(name=product_name,
                                                description=product_description,
                                                )
        return created_product
    
    def _create_price_product(self, product, created_product: stripe.Product) -> stripe.Price:
        """Создание данных о цене
        """
        product_amount = product.amount    
        created_price_product = stripe.Price.create(unit_amount_decimal=product_amount,
                                                    currency='rub',
                                                    product=created_product.id,
                                                    )
        return created_price_product
    
    def _check_product_in_stripe(self, product_name) -> Union[stripe.Price, None]:
        """Проверка нахождения продукта в Stripe
        """        
        get_product = stripe.Product.search(query=f'name~"{product_name}"')
        if get_product:
            get_price = stripe.Price.search(query=f'product:"{get_product.data[0].id}"')
            return get_price

    def __get_product_name(self, product) -> str:
        """Получения имени продукта
        """        
        try:
            product_name = product.course_name
        except:
            product_name = product.lesson_name
        return product_name
    
    def _set_object_stripe(self, product) -> stripe.Price:
        """Точка создания продукта
        """
        product_name = self.__get_product_name(product)  
        stripe_product = self._check_product_in_stripe(product_name)
        if not stripe_product:    
            stripe_product = self._create_product(product, product_name)
            stripe_product_price = self._create_price_product(product, stripe_product)
        else:
            stripe_product_price = stripe_product.data[0]
        return stripe_product_price


class SessionLinkPayment:
    """Класс получения ссылки на оплату
    """
    BASE_URL = settings.ALLOWED_HOSTS if settings.ALLOWED_HOSTS else 'http://127.0.0.1:8000'
    
    def __init__(self, request: Request, product: Union[Course, Lesson]) -> None:
        """Инициализация продукта

        Args:
            product (Union[Course, Lesson]): Продукт типа Course или Lesson
        """        
        if not isinstance(product, Union[Course, Lesson]):
            raise TypeError(f'{product}, должен представлять собой Курс или Урок')
        self.product = product
        self.stripe_item = StripeItem(product)
        if not isinstance(request, Request):
            raise TypeError(f'{request} должен быть классом rest_framework.request.Request')
        self.request = request
        
    def _create_link_payments(self, created_price_product: stripe.Price) -> stripe.PaymentLink:
        """Создание ссылки для оплаты
        """
        id_price_product = created_price_product.id
        created_product_link_payment = stripe.PaymentLink.create(line_items=[{'price': id_price_product,
                                                                              'quantity': 1,
                                                                              }])
        pay_name = f'pay_{self.product._meta.model_name}'
        data = {
            'user': self.request.user,
            'id_session': created_product_link_payment.id,
            pay_name: self.product,
            'payment_amount': self.product.amount,
            'payment_method': 'money_transfer'
        }
        Payments.objects.create(**data)
        return created_product_link_payment
    
    def _create_session_payments(self, created_price_product: stripe.Price) -> stripe.checkout.Session:
        """Создание сессии для оплаты
        """   
        id_price_product = created_price_product.item.id
        success_url = self.BASE_URL + reverse('courses:done_payment')
        cancel_url = self.BASE_URL + reverse('courses:cancel_payment')
        created_sessions_payments = stripe.checkout.Session.create(line_items=[{'price': id_price_product,
                                                                                'quantity': 1,
                                                                                }],
                                                                   mode='payment',
                                                                   success_url=success_url,
                                                                   cancel_url=cancel_url,
                                                                   )
        pay_name = f'pay_{self.product._meta.model_name}'
        data = {
            'user': self.request.user,
            'id_session': created_sessions_payments.id,
            pay_name: self.product,
            'payment_amount': self.product.amount,
            'payment_method': 'money_transfer'
        }
        Payments.objects.create(**data)
        return created_sessions_payments
    
    @classmethod
    def _get_sessions_payment(cls, payment: Payments) -> stripe.checkout.Session:
        """Получение сессии для обработки
        """
        stripe.api_key = find_env('STRIPE_API_KEY')
        id_session = payment.id_session
        session = stripe.checkout.Session.retrieve(id=id_session)
        return session
    
    def get_link(self) -> stripe.PaymentLink:
        """Получить ссылку для оплаты указанного товара
        """     
        product_price = self.stripe_item
        link_to_payment = self._create_link_payments(product_price)
        return link_to_payment
    
    def get_checkout_session(self) -> stripe.checkout.Session:
        """Получить ссылку на сессию оплаты на сайте Stripe
        """
        product_price = self.stripe_item
        session_to_payment = self._create_session_payments(product_price)
        return session_to_payment
    
    @classmethod
    def get_sessions_details(cls, payment: Payments) -> Dict:
        """Получение статусов сессий оплаты
        """
        if not isinstance(payment, Payments):
            raise TypeError(f'{payment}, должен быть классом Payments')
        session = cls._get_sessions_payment(payment=payment)
        customer_details = session.get('customer_details')
        params_session = {
            'id': session.id,
            'amount_total': session.amount_total,
            'automatic_tax': session.automatic_tax.get('enabled'),
            'currency': session.currency.upper(),
            'user_email': customer_details.get('email') if customer_details else None,
            'user_name': customer_details.get('name') if customer_details else None,
            'phone': customer_details.get('phone') if customer_details else None,
            'payment_intent': session.payment_intent,
            'url': session.url,
            'status': session.status.upper()
        }
        return params_session
    