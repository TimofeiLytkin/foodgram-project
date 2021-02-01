from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe

from users.models import User

from recipes.validators import validate_file_size


class Recipe(models.Model):
    """ORM-модель 'Рецепт'."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=100, verbose_name='Название')
    duration = models.SmallIntegerField(verbose_name='Время приготовления')
    text = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    image = models.ImageField(
        upload_to="recipe_images/",
        validators=[validate_file_size],
        verbose_name='Изображение'
    )
    ingredient = models.ManyToManyField(
        "Ingredient",
        related_name="ingredients",
        through="IngredientAmount",
    )

    def __str__(self):
        return self.title

    def image_img(self):
        if self.image:
            return mark_safe(
                f'<img width="90" height="50" src="{self.image.url}" />'
            )
        return 'Без изображения'

    image_img.short_description = 'Изображение'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class Ingredient(models.Model):
    """ORM-модель 'Ингредиент'."""
    title = models.CharField(max_length=100, verbose_name='Название')
    dimension = models.CharField(
        max_length=16, verbose_name='Eдиница измерения'
    )

    def __str__(self):
        return f'{self.title}, {self.dimension}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ('title', 'dimension')
        ordering = ('title',)


class IngredientAmount(models.Model):
    """ORM-модель 'Рецепт - Ингредиент'."""
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantity',
        verbose_name='Рецепт'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(0, 1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Tag(models.Model):
    """ORM-модель 'Тег'."""
    COLOR = {
        'Завтрак': 'orange',
        'Обед': 'green',
        'Ужин': 'purple'
    }
    SLUG = {
        'Завтрак': 'b',
        'Обед': 'l',
        'Ужин': 'd'
    }
    TITLE = (
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин')
    )

    title = models.CharField(
        max_length=50, choices=TITLE, verbose_name='Название'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Рецепт',
    )
    slug = models.SlugField(
        default='', editable=False, max_length=50, verbose_name='Адрес')
    color = models.CharField(
        max_length=50,
        default='',
        editable=False,
        verbose_name='Цвет'
    )

    def __str__(self):
        return self.title

    def _generate_color_and_slug(self):
        value = self.title
        self.color = self.COLOR[value]
        self.slug = self.SLUG[value]

    def save(self, *args, **kwargs):
        self._generate_color_and_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
