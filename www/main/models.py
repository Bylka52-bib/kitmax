from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=[
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
        ('content_manager', 'Контент-менеджер'),
    ], default='student')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    platform_user_id = models.IntegerField(null=True, blank=True, verbose_name='ID в основной платформе')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Course(models.Model):
    platform_course_id = models.IntegerField(unique=True, verbose_name='ID курса в основной платформе')
    title = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=200, blank=True, verbose_name='Краткое описание для лендинга')
    cover_image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Обложка курса')
    preview_video = models.URLField(blank=True, verbose_name='Превью видео')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses', verbose_name='Автор курса')
    total_students = models.PositiveIntegerField(default=0, verbose_name='Всего студентов')
    average_rating = models.FloatField(default=0, verbose_name='Средний рейтинг')
    is_featured = models.BooleanField(default=False, verbose_name='Показывать на лендинге')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_author_name(self):
        if self.author:
            return self.author.name
        return 'Кит Макс'


class Testimonial(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='testimonials',
        verbose_name='Курс'
    )
    guest_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Имя (для гостей)'
    )
    guest_email = models.EmailField(
        blank=True,
        verbose_name='Email (для гостей)'
    )
    content = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name='Рейтинг'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Подтвержден (пользователь действительно прошел курс)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.course.title} ({self.rating})"
        return f"{self.guest_name} - {self.course.title} ({self.rating})"

    @property
    def display_name(self):
        if self.user:
            return self.user.first_name or self.user.email
        return self.guest_name or "Аноним"


class Lead(models.Model):
    USER_TYPES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('contacted', 'Связались'),
        ('converted', 'Конвертирован в пользователя'),
        ('lost', 'Потерян'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Интересующий курс'
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-\(\)]+$',
                message='Введите корректный номер телефона'
            )
        ]
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        verbose_name='Тип пользователя'
    )
    message = models.TextField(blank=True, verbose_name='Сообщение')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий менеджера')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_user_type_display()})"

    def save(self, *args, **kwargs):
        if not self.user and self.email:
            try:
                self.user = User.objects.get(email=self.email)
            except User.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class PlatformStatistics(models.Model):
    active_courses = models.PositiveIntegerField(default=0, verbose_name='Активные курсы')
    total_students = models.PositiveIntegerField(default=0, verbose_name='Всего студентов')
    total_teachers = models.PositiveIntegerField(default=0, verbose_name='Всего преподавателей')
    completed_duels = models.PositiveIntegerField(default=0, verbose_name='Проведено дуэлей')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Статистика платформы'
        verbose_name_plural = 'Статистика платформы'

    def __str__(self):
        return f"Статистика от {self.updated_at}"


class HeroBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    subtitle = models.TextField(verbose_name='Подзаголовок')
    background_image = models.ImageField(upload_to='hero/', blank=True, verbose_name='Фоновое изображение')
    button_text = models.CharField(max_length=50, default='Начать обучение', verbose_name='Текст кнопки')
    button_link = models.CharField(max_length=200, default='/auth', verbose_name='Ссылка кнопки')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Hero блок'
        verbose_name_plural = 'Hero блоки'

    def __str__(self):
        return self.title


class StudentBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    icon = models.FileField(
        upload_to='icons/',
        blank=True,
        verbose_name='Иконка (PNG, JPG, SVG)',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg'])]
    )
    featured_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='student_blocks',
        verbose_name='Рекомендуемые курсы'
    )

    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Блок "Для студентов"'
        verbose_name_plural = 'Блоки "Для студентов"'
        ordering = ['order']

    def __str__(self):
        return self.title


class TeacherBlock(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    icon = models.FileField(
        upload_to='icons/',
        blank=True,
        verbose_name='Иконка (PNG, JPG, SVG)',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg'])]
    )
    feature_link = models.URLField(blank=True, verbose_name='Ссылка на инструмент')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Блок "Для преподавателей"'
        verbose_name_plural = 'Блоки "Для преподавателей"'
        ordering = ['order']

    def __str__(self):
        return self.title


class Screenshot(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='screenshots/', verbose_name='Скриншот')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='screenshots',
        verbose_name='Курс'
    )

    section = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Для студентов'),
            ('teacher', 'Для преподавателей'),
        ],
        verbose_name='Раздел'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'
        ordering = ['section', 'order']

    def __str__(self):
        return f"{self.title} - {self.get_section_display()}"


class PricingPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тарифа')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    price_period = models.CharField(max_length=20, default='месяц', verbose_name='Период оплаты')
    features = models.JSONField(default=list, verbose_name='Возможности')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'
        ordering = ['order']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя автора')
    bio = models.TextField(blank=True, verbose_name='Биография')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название книги')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор'
    )
    pages = models.IntegerField(verbose_name='Количество страниц')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    published_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
