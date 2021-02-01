from django.core.exceptions import ValidationError
from django.db import models

from recipes.models import Recipe
from users.models import User


class Favorite(models.Model):
    """ORM-модель 'Избранное'."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
    )

    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.recipe.title}'

    def clean(self):
        if self.user.username == self.recipe.author.username:
            raise ValidationError(
                'Нельзя добавлять в избранное собственные рецепты'
            )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'recipe')


class Subscribe(models.Model):
    """ORM-модель 'Подписка'."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'

    def clean(self):
        if self.author == self.user:
            raise ValidationError('Нельзя подписываться на самого себя')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')


class Purchase(models.Model):
    """ORM-модель 'Покупка'."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_purchases',
    )

    def __str__(self):
        return f'{self.user.username} добавил в покупки {self.recipe.title}'

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = ('user', 'recipe')
