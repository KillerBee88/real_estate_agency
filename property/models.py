from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


class Flat(models.Model):
    owner = models.CharField('ФИО владельца', max_length=200)
    owners_phonenumber = models.CharField('Номер владельца', max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.NullBooleanField('Наличие балкона', db_index=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    new_building = models.BooleanField(
        'Новостройка',
        null=True,
        default=None,
        db_index=True)
    likes = models.ManyToManyField(User, related_name='liked_flats', blank=True)
    owner_normalized_phone = PhoneNumberField('Нормальный номер владельца', blank=True, null=True)

   

    def clean(self):
            if self.owners_phonenumber:
                try:
                    phone_number = phonenumbers.parse(self.owners_phonenumber, 'RU')
                    if not phonenumbers.is_valid_number(phone_number):
                        raise ValidationError("The phone number entered is not valid.")
                except phonenumbers.phonenumberutil.NumberParseException:
                    raise ValidationError("The phone number entered is not valid.")


    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто жаловался: ')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира, на которую пожаловались: ')
    text = models.TextField('Текст жалобы: ')


    def __str__(self):
        return f'{self.user.username} - {self.flat}'
    
class Owner(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    phonenumber = models.CharField("Номер телефона", max_length=15)
    normalized_phonenumber = models.CharField("Нормализованный номер телефона", max_length=15)
    flats = models.ManyToManyField(Flat, related_name="owners", verbose_name="Квартиры")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Собственник"
        verbose_name_plural = "Собственники"
