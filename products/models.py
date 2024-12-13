from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField('Название подкатегории', max_length=100)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField('Бренд', max_length=100)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, verbose_name='Подкатегория', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Название товара', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    available = models.BooleanField('Доступен', default=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f"Изображение для {self.product.name}"

class Size(models.Model):
    name = models.CharField('Размер', max_length=10)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField('Цвет', max_length=30)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, verbose_name='Размер', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name='Цвет', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField('Количество на складе', default=0)

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.color.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField('Отзыв')
    rating = models.PositiveIntegerField('Оценка', default=5)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('product', 'user')
        ordering = ['-created']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"