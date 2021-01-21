from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile

class TestUserprofile(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_bob = User.objects.create_user('Bob')
        self.user_alice = User.objects.create_user('Alice')
        self.superuser = User.objects.create_superuser('root')

    def test_profile(self):
        self.assertIsInstance(self.user_bob.profile, Profile)
        self.assertIsInstance(self.superuser.profile, Profile)

class TestTemplates(TestUserprofile):
    def http_code_test(self, url, code=200):
        return self.assertEqual(self.client.get(url).status_code, code)

    def test_templates(self):
        url_register = reverse('userprofile:register')
        url_login = reverse('userprofile:login')
        url_detail = reverse('userprofile:detail', args=(self.user_bob.profile.id,))

        self.http_code_test(url_register, 200)
        self.http_code_test(url_login, 200)
        self.http_code_test(url_detail, 200)

    def test_logged_templates(self):
        url_logout = reverse('userprofile:logout')
        url_edit_bob = reverse('userprofile:edit', args=(self.user_bob.profile.id,))
        url_edit_alice = reverse('userprofile:edit', args=(self.user_alice.profile.id,))

        self.http_code_test(url_edit_bob, 302)
        self.http_code_test(url_logout, 302)

        self.client.force_login(self.user_bob)

        self.http_code_test(url_edit_bob, 200)
        self.http_code_test(url_edit_alice, 403)

        # POST only
        self.http_code_test(url_logout, 403)
        self.assertEqual(self.client.post(url_logout).status_code, 302)
