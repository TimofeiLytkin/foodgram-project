from django.test import Client, TestCase
from django.urls import reverse

from recipes.models import Recipe
from users.models import User


class TestFavorite(TestCase):
    """Проверка добавления рецепта в избранное."""

    def setUp(self):
        self.auth_client = Client()
        self.nonauth_client = Client()

        self.user1 = User.objects.create_user(
            username='user1', email='user1@user1.com', password='1234567'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@user2.com', password='123456'
        )
        self.recipe1 = Recipe.objects.create(
            author=self.user1, duration=10, title='title1', text='text1'
            )
        self.recipe2 = Recipe.objects.create(
            author=self.user2, duration=10, title='title2', text='text2'
            )

        self.auth_client.force_login(self.user1)

    def test_follow_favorite(self):
        response = self.nonauth_client.post(
            reverse('favorite_create'), data={'id': self.recipe1.id}
        )
        assert response.status_code == 403, (
            'Незалогиненный пользователь не может добавить рецепт в избранное'
        )

        response = self.auth_client.post(
            reverse('favorite_create'), data={'id': self.recipe2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может добавить не свой рецепт '
            'в избранное'
        )
        assert response.data == {'success': True}, (
            'В ответе должен быть True при успешном добавлении'
        )

        response = self.auth_client.post(
            reverse('favorite_create'), data={'id': self.recipe2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может добавить '
            'не свой рецепт в избранное'
        )
        assert response.data == {'success': False}, (
            'Пользователь не может добавить рецепт в избранное второй раз'
        )

        response = self.auth_client.post(
            reverse('favorite_create'), data={'id': self.recipe1.id}
        )
        assert response.data == {'success': False}, (
            'Пользователь не может добавить в избранное свой рецепт'
        )

    def test_unfollow_favorite(self):
        self.auth_client.post(
            reverse('favorite_create'), data={'id': self.recipe2.id}
        )
        assert self.user1.favorites.count() == 1, (
            'Проверьте, что вы подписаны'
        )

        self.auth_client.delete(
            reverse('favorite_delete', kwargs={'id': self.recipe2.id})
        )
        assert self.user1.favorites.count() == 0, (
            'Проверьте, что вы отписались'
        )


class TestPurchase(TestCase):
    """Проверка добавления рецепта в список покупок."""

    def setUp(self):
        self.auth_client = Client()
        self.nonauth_client = Client()

        self.user1 = User.objects.create_user(
            username='user1', email='user1@user1.com', password='1234567'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@user2.com', password='123456'
        )
        self.recipe1 = Recipe.objects.create(
            author=self.user1, duration=10, title='title1', text='text1'
            )
        self.recipe2 = Recipe.objects.create(
            author=self.user2, duration=10, title='title2', text='text1'
            )

        self.auth_client.force_login(self.user1)

    def test_add_to_purchase(self):
        response = self.nonauth_client.post(
            reverse('purchase_create'), data={'id': self.recipe2.id}
        )
        assert response.status_code == 403, (
            'Незалогиненный пользователь не может добавить рецепт в покупки'
        )

        response = self.auth_client.post(
            reverse('purchase_create'), data={'id': self.recipe2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может добавить рецепт в покупки'
        )
        assert response.data == {'success': True}, (
            'В ответе должен быть True при успешном добавлении'
        )

        response = self.auth_client.post(
            reverse('purchase_create'), data={'id': self.recipe2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может добавить рецепт в покупки'
        )
        assert response.data == {'success': False}, (
            'Пользователь не может добавить рецепт в покупки второй раз'
        )

        response = self.auth_client.post(
            reverse('purchase_create'), data={'id': self.recipe1.id}
        )
        assert response.data == {'success': True}, (
            'Пользователь может добавить в покупки свой рецепт'
        )

    def test_remove_to_purchase(self):
        self.auth_client.post(
            reverse('purchase_create'), data={'id': self.recipe2.id}
        )
        assert self.user1.purchases.count() == 1, (
            'Проверьте, что вы подписаны'
        )

        self.auth_client.delete(
            reverse('purchase_delete', kwargs={'id': self.recipe2.id})
        )
        assert self.user1.purchases.count() == 0, (
            'Проверьте, что вы отписались'
        )


class TestSubscribe(TestCase):
    """Проверка правильности работы системы подписок."""

    def setUp(self):
        self.auth_client = Client()
        self.nonauth_client = Client()

        self.user1 = User.objects.create_user(
            username='user1', email='user1@user1.com', password='1234567'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@user2.com', password='123456'
        )

        self.auth_client.force_login(self.user1)

    def test_follow_author(self):
        response = self.nonauth_client.post(
            reverse('subscribe_create'), data={'id': self.user2.id}
        )
        assert response.status_code == 403, (
            'Незалогиненный пользователь не может подписаться на авторов'
        )

        response = self.auth_client.post(
            reverse('subscribe_create'), data={'id': self.user2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может подписаться на авторов'
        )
        assert response.data == {'success': True}, (
            'В ответе должен быть True при успешной подписке'
        )

        response = self.auth_client.post(
            reverse('subscribe_create'), data={'id': self.user2.id}
        )
        assert response.status_code == 200, (
            'Залогиненный пользователь может подписаться на авторов'
        )
        assert response.data == {'success': False}, (
            'Пользователь не может подписаться второй раз на себя'
        )

        response = self.auth_client.post(
            reverse('subscribe_create'), data={'id': self.user1.id}
        )
        assert response.data == {'success': False}, (
            'Пользователь не может подписаться на себя'
        )

    def test_unfollow_author(self):
        self.auth_client.post(
            reverse('subscribe_create'), data={'id': self.user2.id}
        )
        assert self.user1.follower.count() == 1, (
            'Проверьте, что вы подписаны'
        )

        self.auth_client.delete(
            reverse('subscribe_delete', kwargs={'id': self.user2.id})
        )
        assert self.user1.follower.count() == 0, (
            'Проверьте, что вы отписались'
        )
