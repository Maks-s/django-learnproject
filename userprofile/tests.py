from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile
from .forms import ProfileEditForm, ProfileLoginForm, ProfileRegisterForm

class TestUserprofile(TestCase):
    # Global data used across all tests
    @classmethod
    def setUpTestData(cls):
        cls.user_bob = User.objects.create_user('Bob')
        cls.user_alice = User.objects.create_user('Alice')
        cls.superuser = User.objects.create_superuser('root')

        cls.url_register = reverse('userprofile:register')
        cls.url_login = reverse('userprofile:login')
        cls.url_detail = reverse('userprofile:detail', args=(cls.user_bob.profile.id,))
        cls.url_logout = reverse('userprofile:logout')
        cls.url_edit_bob = reverse('userprofile:edit', args=(cls.user_bob.profile.id,))

        return super(TestUserprofile, cls).setUpTestData()

    def assertGetHTTPCode(self, url, code=200):
        return self.assertEqual(self.client.get(url).status_code, code)

    def assertPostHTTPCode(self, url, data={}, code=200):
        return self.assertEqual(self.client.post(url, data).status_code, code)

# Generic tests
class TestTemplates(TestUserprofile):
    def test_templates(self):
        self.assertGetHTTPCode(self.url_register, 200)
        self.assertGetHTTPCode(self.url_login, 200)
        self.assertGetHTTPCode(self.url_detail, 200)
        self.assertGetHTTPCode(self.url_logout, 302)

class TestModels(TestUserprofile):
    def test_profile_model(self):
        self.assertIsInstance(self.user_bob.profile, Profile)
        self.assertIsInstance(self.superuser.profile, Profile)

# Views tests
class TestProfileRegister(TestUserprofile):
    def test_register(self):
        data = {
            'username': 'Test',
            'password1': 'rokkenjima',
            'password2': 'rokkenjima'
        }

        self.assertPostHTTPCode(self.url_register, data, 302)
        self.assertTrue(self.client.login(username='Test', password='rokkenjima'))

        # Logged-in users shouldn't be able to register
        self.assertGetHTTPCode(self.url_register, 302)

    def test_invalid_register(self):
        data = {
            'username': 'Test',
            'password1': 'aaaaaaaaaa',
            'password2': ''
        }

        self.assertPostHTTPCode(self.url_register, data, 200)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=data['username'])

class TestProfileLogin(TestUserprofile):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'Credential',
            'password': 'Credential'
        }
        User.objects.create_user(**cls.credentials)

        return super(TestProfileLogin, cls).setUpTestData()

    def test_login(self):
        self.assertPostHTTPCode(self.url_login, self.credentials, 302)

    def test_invalid_login(self):
        data = {
            'username': 'invalid',
            'password': 'invalid'
        }

        self.assertPostHTTPCode(self.url_login, data, 200)

class TestProfileLogout(TestUserprofile):
    def test_logout(self):
        # Anonymous
        self.assertGetHTTPCode(self.url_logout, 302)

        self.client.force_login(self.user_bob)

        # POST only
        self.assertGetHTTPCode(self.url_logout, 403)
        self.assertPostHTTPCode(self.url_logout, code=302)

class TestProfileEditView(TestUserprofile):
    def test_profile_edit_authorization(self):
        # Anonymous
        self.assertGetHTTPCode(self.url_edit_bob, 302)

        # Other user
        self.client.force_login(self.user_alice)
        self.assertGetHTTPCode(self.url_edit_bob, 403)
        self.assertPostHTTPCode(self.url_edit_bob, code=403)

        # Same user
        self.client.force_login(self.user_bob)
        self.assertGetHTTPCode(self.url_edit_bob, 200)
        self.assertPostHTTPCode(self.url_edit_bob, code=302)

        # Admin
        self.client.force_login(self.superuser)
        self.assertGetHTTPCode(self.url_edit_bob, 200)
        self.assertPostHTTPCode(self.url_edit_bob, code=302)

    def test_profile_user_edit(self):
        self.client.force_login(self.user_bob)
        data = {
            'bio': 'Hey'
        }

        response = self.client.post(self.url_edit_bob, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.get(user=self.user_bob).bio, data['bio'])

    def test_profile_superuser_edit(self):
        self.client.force_login(self.superuser)
        data = {
            'bio': 'Admin changed'
        }

        response = self.client.post(self.url_edit_bob, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.get(user=self.user_bob).bio, data['bio'])

# Forms tests
class TestProfileEditForm(TestUserprofile):
    def test_valid_profile_edit_form(self):
        form = ProfileEditForm(
            data = {
                'user': self.user_bob
            },
            instance = self.user_bob.profile
        )

        self.assertTrue(form.is_valid())

    def test_default_bio(self):
        self.user_bob.profile.bio = 'Test'

        form = ProfileEditForm(
            data = {
                'user': self.user_bob
            },
            instance = self.user_bob.profile
        )

        self.assertEqual(form.fields['bio'].initial, self.user_bob.profile.bio)
