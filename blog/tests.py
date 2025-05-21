from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment
from rest_framework_simplejwt.tokens import RefreshToken

class BlogAPITestCase(APITestCase):
    def setUp(self):
        # Створюємо користувачів
        self.user = User.objects.create_user(username='user1', password='pass1234')
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_staff=True)

        # Токени
        self.user_token = self.get_token(self.user)
        self.admin_token = self.get_token(self.admin)

        # Створюємо пост для тестів
        self.post = Post.objects.create(
            title='Test Post',
            content='Some content',
            author=self.user,
            category='TestCategory'
        )
        # Створюємо коментар
        self.comment = Comment.objects.create(
            post=self.post,
            author_name='Commenter',
            content='Nice post!'
        )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # --- Тести Post ---

    def test_post_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('post-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_post_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('post-list-create')
        data = {
            "title": "New Post",
            "content": "New content",
            "author": self.user.id,  # Якщо автор задається автоматично, це поле можна виключити
            "category": "NewCategory"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')

    def test_post_detail_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_post_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('post-detail', args=[self.post.id])
        data = {
            "title": "Updated Post",
            "content": self.post.content,
            "author": self.user.id,
            "category": self.post.category
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')

    def test_post_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Тести Comment ---

    def test_comment_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('comment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_comment_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('comment-list-create')
        data = {
            "post": self.post.id,
            "author_name": "Tester",
            "content": "Great post!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author_name'], 'Tester')

    def test_comment_detail_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author_name'], self.comment.author_name)

    def test_comment_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('comment-detail', args=[self.comment.id])
        data = {
            "post": self.post.id,
            "author_name": self.comment.author_name,
            "content": "Updated comment"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated comment')

    def test_comment_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Тести реєстрації та логіну ---

    def test_register(self):
        url = reverse('auth_register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            "username": self.user.username,
            "password": "pass1234"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # --- Тест доступу для admin-only ---

    def test_admin_only_access_for_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        url = reverse('admin-only')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Привіт, адміністраторе!')

    def test_admin_only_access_for_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('admin-only')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_only_access_unauthenticated(self):
        url = reverse('admin-only')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
