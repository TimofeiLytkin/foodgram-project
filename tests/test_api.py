from django.test import Client, TestCase

from recipes.models import Recipe
from users.models import User


class TestFavorite(TestCase):
    """Проверка добавления рецепта в избранное."""

    def setUp(self):
        self.client = Client()
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

    def test_follow_favorite(self):
        response = self.client.post("/api/v1/favorites/", {"id": 1})
        assert response.status_code == 403, \
            'Незалогиненный пользователь не может добавить рецепт в избранное'

        self.client.login(username='user1', password='1234567')
        response = self.client.post("/api/v1/favorites/", {"id": 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может добавить не свой рецепт в избранное'
        assert response.data == {'success': True}, \
            'В ответе должен быть True при успешном добавлении'

        response = self.client.post("/api/v1/favorites/", {"id": 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может добавить не свой рецепт в избранное'
        assert response.data == {'success': False}, \
            'Пользователь не может добавить рецепт в избранное второй раз'

        response = self.client.post("/api/v1/favorites/", {"id": 1})
        assert response.data == {'success': False}, \
            'Пользователь не может добавить в избранное свой рецепт'

    def test_unfollow_favorite(self):
        self.client.login(username='user1', password='1234567')

        self.client.post('/api/v1/favorites/', {'id': 2})
        assert self.user1.favorites.count() == 1, \
            'Проверьте, что вы подписаны'

        self.client.delete('/api/v1/favorites/2/')
        assert self.user1.favorites.count() == 0, \
            'Проверьте, что вы отписались'


class TestPurchase(TestCase):
    """Проверка добавления рецепта в список покупок."""

    def setUp(self):
        self.client = Client()
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

    def test_add_to_purchase(self):
        response = self.client.post("/api/v1/purchases/")
        assert response.status_code == 403, \
            'Незалогиненный пользователь не может добавить рецепт в покупки'

        self.client.login(username='user1', password='1234567')
        response = self.client.post("/api/v1/purchases/", {"id": 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может добавить рецепт в покупки'
        assert response.data == {'success': True}, \
            'В ответе должен быть True при успешном добавлении'

        response = self.client.post("/api/v1/purchases/", {"id": 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может добавить рецепт в покупки'
        assert response.data == {'success': False}, \
            'Пользователь не может добавить рецепт в покупки второй раз'

        response = self.client.post("/api/v1/purchases/", {"id": 1})
        assert response.data == {'success': True}, \
            'Пользователь может добавить в покупки свой рецепт'

    def test_remove_to_purchase(self):
        self.client.login(username='user1', password='1234567')

        self.client.post('/api/v1/purchases/', {'id': 2})
        assert self.user1.purchases.count() == 1, \
            'Проверьте, что вы подписаны'

        self.client.delete('/api/v1/purchases/2/')
        assert self.user1.purchases.count() == 0, \
            'Проверьте, что вы отписались'


class TestSubscribe(TestCase):
    """Проверка правильности работы системы подписок."""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1', email='user1@user1.com', password='1234567'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@user2.com', password='123456'
        )

    def test_follow_author(self):
        response = self.client.post('/api/v1/subscriptions/', {'id': 2})
        assert response.status_code == 403, \
            'Незалогиненный пользователь не может подписаться на авторов'

        self.client.login(username='user1', password='1234567')
        response = self.client.post('/api/v1/subscriptions/', {'id': 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может подписаться на авторов'
        assert response.data == {'success': True}, \
            'В ответе должен быть True при успешной подписке'

        response = self.client.post('/api/v1/subscriptions/', {'id': 2})
        assert response.status_code == 200, \
            'Залогиненный пользователь может подписаться на авторов'
        assert response.data == {'success': False}, \
            'Пользователь не может подписаться второй раз на себя'

        response = self.client.post('/api/v1/subscriptions/', {'id': 1})
        assert response.data == {'success': False}, \
            'Пользователь не может подписаться на себя'

    def test_unfollow_author(self):
        self.client.login(username='user1', password='1234567')

        self.client.post('/api/v1/subscriptions/', {'id': 2})
        assert self.user1.follower.count() == 1, \
            'Проверьте, что вы подписаны'

        self.client.delete('/api/v1/subscriptions/2/')
        assert self.user1.follower.count() == 0, \
            'Проверьте, что вы отписались'
