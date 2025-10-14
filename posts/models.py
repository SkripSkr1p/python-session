from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Модель категории объявлений"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель объявления"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Контактный телефон")
    contact_email = models.EmailField(blank=True, verbose_name="Контактный email")
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """Модель комментария к объявлению"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Объявление")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Содержание комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.post.title}'
