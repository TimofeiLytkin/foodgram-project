import io

from django.core.files.base import ContentFile
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from users.models import User
from recipes.models import Recipe


class TestUser(TestCase):
    def setUp(self):
        self.auth_client = Client()
        self.nonauth_client = Client()

        self.user = User.objects.create_user(
            'user1', 'user1@test.com', '12345'
        )
        self.user.save()
        self.auth_client.force_login(self.user)
        self.user_not_found = 'user2'

    def get_image(self):
        buffer = io.BytesIO()
        img = Image.new('RGB', (500, 500), (0, 0, 0))
        img.save(buffer, format='jpeg')
        buffer.seek(0)
        image = ContentFile(buffer.read(), name='test.jpeg')
        return image

    def test_profile_page(self):
        response = self.auth_client.get(
            reverse('profile', kwargs={'username': self.user})
        )
        assert response.status_code == 200, (
            'Пользователь не может перейти на страницу зарег. пользователя'
        )
        assert response.context['username'] == self.user.username, (
            'Username из url не совпадает с тем что на странице'
        )

    def test_error_404(self):
        response = self.auth_client.get(
            reverse('profile', kwargs={'username': self.user_not_found})
        )

        assert response.status_code == 404, (
            'При доступе к страницы несуществующего пользователя не '
            'возвращается ошибка 404'
        )

    def test_auth_client_create_recipe_post(self):
        self.auth_client.post(
            reverse('create_recipe'),
            data={
                'title': 'title1',
                'tag': 'Завтрак',
                'duration': 1,
                'text': 'text1',
                'image': self.get_image()
            }
        )
        recipes = Recipe.objects.all()
        assert 'text1' in [recipe.text for recipe in recipes], (
            'Текс созданного рецепта не совпадает с тем что в БД (POST)'
        )
        assert recipes.count() == 1, (
            'Рецепт не был создан зарегестрированным пользователем (POST)'
        )

    def test_auth_client_create_recipe_get(self):
        self.auth_client.get(
            reverse('create_recipe'),
            data={
                'title': 'title1',
                'duration': 1,
                'text': 'text1',
                'image': self.get_image()
            }
        )
        recipes = Recipe.objects.all()
        assert recipes.count() == 0, (
            'Рецепт был создан зарегестрированным пользователем (GET)'
        )

    def test_nonauth_client_create_recipe_post(self):
        self.nonauth_client.post(
            reverse('create_recipe'),
            data={
                'title': 'title1',
                'duration': 1,
                'text': 'text1',
                'image': self.get_image()
            }
        )
        recipes = Recipe.objects.all()
        assert recipes.count() == 0, (
            'Рецепт был создан незарегестрированным пользователем (POST)'
        )

        response = self.nonauth_client.get(reverse('create_recipe'))
        assert response.status_code == 302, (
            'Незарегестрированный пользователь при попытке создать рецепт '
            'не был перенаправлен (POST)'
        )

    def test_nonauth_client_create_recipe_get(self):
        self.nonauth_client.get(
            reverse('create_recipe'),
            data={
                'title': 'title1',
                'tag': 'Завтрак',
                'duration': 1,
                'text': 'text1',
                'image': self.get_image()
            }
        )

        recipes = Recipe.objects.all()
        assert recipes.count() == 0, (
            'Рецепт был создан незарегестрированным пользователем (GET)'
        )

        response = self.nonauth_client.get(reverse('create_recipe'))
        assert response.status_code == 302, (
            'Незарегестрированный пользователь при попытке создать рецепт '
            'не был перенаправлен (GET)'
        )
