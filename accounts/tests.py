from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile

class AccountsTests(TestCase):
    def setUp(self):
        # Създаване на тестов потребител
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = Profile.objects.get(user=self.user)

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Пренасочване след успешен вход
        self.assertTrue('_auth_user_id' in self.client.session)  # Проверка за активна сесия

    def test_logout_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Пренасочване след изход
        self.assertFalse('_auth_user_id' in self.client.session)  # Проверка за излязъл потребител

    def test_change_password(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('password_reset'), {
            'old_password': 'testpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Пренасочване след успешна смяна на парола
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Успешно рендиране на страницата
        self.assertTemplateUsed(response, 'profile.html')  # Проверка за правилния шаблон


class EditProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.edit_profile_url = reverse('edit_profile')

    def test_edit_profile(self):
        response = self.client.post(self.edit_profile_url, {
            'username': 'newusername',
            'bio': 'Updated bio',
            'phone_number': '123456789'
        })
        self.assertEqual(response.status_code, 302)  # Очаквано пренасочване
        self.user.refresh_from_db()  # Обновяване на потребителя от базата данни
        self.assertEqual(self.user.username, 'newusername')  # Проверка за обновеното потребителско име

class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'email': 'testuser@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Проверка за пренасочване
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Проверка за създаване на потребител






