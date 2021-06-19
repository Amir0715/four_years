import hashlib
import random
import sys

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0, sys.maxsize)).encode('utf-8'))
    return hash.hexdigest()


class Address(models.Model):
    region = models.CharField(verbose_name='Регион', max_length=22, null=True, blank=True)
    locality = models.CharField(verbose_name='Населенный пункт', max_length=100, null=True, blank=True)
    street = models.CharField(verbose_name='Улица', max_length=100, null=True, blank=True)
    house = models.CharField(verbose_name='Дом', max_length=20, null=True, blank=True)
    housing = models.CharField(verbose_name='Корпус', max_length=20, null=True, blank=True)
    index = models.CharField(verbose_name='Индекс', max_length=6, validators=[MinLengthValidator(6), ],
                             null=True, blank=True)
    numbers_house = models.CharField(verbose_name='Квартира', max_length=3, validators=[MinLengthValidator(3)],
                                     null=True, blank=True)

    class Meta:
        ordering = ['region']
        verbose_name = 'Адресс'
        verbose_name_plural = 'Адресс'

    def __str__(self):
        return ', '.join(
            [self.region, self.locality, self.street, self.house, self.housing, self.index, self.numbers_house])


class University(models.Model):
    name = models.CharField(verbose_name='Университет', max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'


class Specialization(models.Model):
    specialization = models.CharField(verbose_name='Название', max_length=25)
    description = models.CharField(verbose_name='Описание', max_length=150)
    university = models.ForeignKey('University', on_delete=models.CASCADE)

    def __str__(self):
        return self.specialization

    class Meta:
        ordering = ['specialization']
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


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

    choice = models.ForeignKey('Specialization', on_delete=models.CASCADE, null=True, blank=True)

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


def user_directory_path(instance, filename):
    # Метод для формирование пути сохранения для файлов
    return f'application/{instance.id_user}/{filename}'


class Application(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_address = models.ForeignKey('Address', on_delete=models.CASCADE)

    status = models.BooleanField(default=False)
    creature_date = models.DateTimeField(auto_now_add=True)

    file_passport = models.FileField(verbose_name='Паспорт', upload_to=user_directory_path)
    file_certificate = models.FileField(verbose_name='Атестат', upload_to=user_directory_path)
    file_statement = models.FileField(verbose_name='Заявление', upload_to=user_directory_path)
    file_other = models.FileField(verbose_name='Другие документы', blank=True, null=True, upload_to=user_directory_path)

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'
