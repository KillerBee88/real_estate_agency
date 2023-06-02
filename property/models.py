from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


class Owner(models.Model):
    full_name = models.CharField('ФИО владельца', max_length=200)
    phonenumber = PhoneNumberField('Номер владельца', blank=True, null=True)
    normalized_phonenumber = PhoneNumberField('Нормализованный номер владельца', blank=True, null=True)

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class Flat(models.Model):
    owners = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='flats', null=True)
    created_at = models.DateTimeField(
        'Дата создания объявления',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Описание квартиры', blank=True)
    price = models.IntegerField('Цена', db_index=True)

    town = models.CharField(
        'Город',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат',
        db_index=True)
    living_area = models.IntegerField(
        'Жилая площадь',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Балкон', db_index=True)
    active = models.BooleanField('Активное объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки',
        null=True,
        blank=True,
        db_index=True)
    new_building = models.BooleanField(
        'Новостройка',
        null=True,
        default=None,
        db_index=True)
    likes = models.ManyToManyField(User, related_name='liked_flats', blank=True, verbose_name='Лайки')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'

    def clean(self):
        if self.owners_phonenumber:
            try:
                phone_number = phonenumbers.parse(self.owners_phonenumber, 'RU')
                if not phonenumbers.is_valid_number(phone_number):
                    raise ValidationError("The phone number entered is not valid.")
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValidationError("The phone number entered is not valid.")


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто жаловался', related_name='complaints')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира, на которую пожаловались', related_name='complaints')

    text = models.TextField('Текст жалобы')
    created_at = models.DateTimeField(
        'Дата создания жалобы',
        default=timezone.now,
        db_index=True)

    def __str__(self):
        return f"Жалоба от {self.user.username} на объявление {self.flat.id}"

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
