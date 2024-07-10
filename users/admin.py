from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, Payments
# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('pk',
                    'username',
                    'avatar',
                    'email',
                    'phone',
                    'city',
                    'first_name',
                    'last_name',
                    'password',
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'date_joined',
                    'last_login',
                    )
    
    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'email',
                     'phone',
                     )
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone", "city", "avatar",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    
@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_pay', 'pay_course', 'pay_lesson', 'payment_amount', 'payment_method', )
    