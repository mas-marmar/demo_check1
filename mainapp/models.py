from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    first_name = None
    last_name = None
    
    fio = models.CharField('ФИО', max_length=255, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    phone = models.CharField('Контактный номер телефона', max_length=20, blank=True, null=True)
    email = models.EmailField('E-mail', unique=True)

    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9]{6,}$')]
    )

    def __str__(self):
        return self.username

class Request(models.Model):
    TRANSPORT_CHOICES = [
        ('kater', 'Катер'),
        ('la liner', 'Круизный лайнер'),
        ('yahta', 'Яхта'),
    ]
    STATUS_CHOICES = [
        (0, 'Новая'),
        (1, 'Идет обучение'),
        (2, 'Обучение завершено'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    transport = models.CharField('Вид транспорта', max_length=20, choices=TRANSPORT_CHOICES)
    start_date = models.DateField('Дата старта занятий')
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_CHOICES)
    status = models.IntegerField('Статус', choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"{self.user.fio} - {self.get_transport_display()}"

class Review(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Отзыв к заявке {self.request.id}"