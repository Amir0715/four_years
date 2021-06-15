from django.core.validators import RegexValidator, MinLengthValidator
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class Address(models.Model):
    region = models.CharField(verbose_name='Школа', max_length=22, null=True, blank=True)
    locality = models.CharField(verbose_name='Регион', max_length=100, null=True, blank=True)
    street = models.CharField(verbose_name='Улица', max_length=100, null=True, blank=True)
    house = models.CharField(verbose_name='Дом', max_length=20, null=True, blank=True)
    housing = models.CharField(verbose_name='Корпус', max_length=20, null=True, blank=True)
    index = models.CharField(verbose_name='Индекс', max_length=6, validators=[MinLengthValidator(6)],
                             null=True, blank=True)
    numbers_house = models.CharField(verbose_name='Квартира', max_length=3, validators=[MinLengthValidator(3)],
                                     null=True, blank=True)


class Choice(models.Model):
    title_choice = models.CharField(verbose_name='Название', max_length=25)
    description_choice = models.CharField(verbose_name='Описание', max_length=150)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an Email')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(
            email,
            password,
            **kwargs
        )


class User(AbstractBaseUser, PermissionsMixin):
    # главнные поля для регистрации
    email = models.EmailField(verbose_name='Электронная почта', max_length=30, unique=True)
    first_name = models.CharField(verbose_name='Фамилия', max_length=22)
    last_name = models.CharField(verbose_name='Имя', max_length=22)

    # профиль

    patronymic = models.CharField(verbose_name='Отчество', max_length=22, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    series_passport = models.CharField(verbose_name='Серия паспорта', max_length=4,
                                       validators=[RegexValidator(r'^\d{1,10}$'), MinLengthValidator(4)], null=True,
                                       blank=True)
    number_passport = models.CharField(verbose_name='Номер паспорта', max_length=6,
                                       validators=[RegexValidator(r'^\d{1,10}$'), MinLengthValidator(6)], null=True,
                                       blank=True)
    school = models.CharField(verbose_name='Школа', max_length=150, null=True, blank=True)

    choice = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)

    # служебнные
    last_time_visit = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ApplicationForm(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_address = models.ForeignKey('Address', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    creature_date = models.DateTimeField(auto_now_add=True)
