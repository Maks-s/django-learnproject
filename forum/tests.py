from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post
from .forms import PostForm

class TestForum(TestCase):
    # Global data used across all tests
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('Bob')
        cls.superuser = User.objects.create_superuser('root')

        cls.post = Post.objects.create(
            author = cls.user,
            title = 'test',
            message = 'This is a test message to test things out'
        )

        cls.url_post_list = reverse('forum:post-list')
        cls.url_post_create = reverse('forum:post-create')
        cls.url_post_detail = reverse('forum:post-detail', args=(cls.post.id,))

        return super(TestForum, cls).setUpTestData()

    def assertGetHTTPCode(self, url, code=200):
        return self.assertEqual(self.client.get(url).status_code, code)

    def assertPostHTTPCode(self, url, data={}, code=200):
        return self.assertEqual(self.client.post(url, data).status_code, code)

# Generic tests
class TestTemplates(TestForum):
    def test_templates(self):
        self.assertGetHTTPCode(self.url_post_list, 200)
        self.assertGetHTTPCode(self.url_post_detail, 200)

# Views tests
class TestPostCreateView(TestForum):
    def test_post_authorization(self):
        self.assertGetHTTPCode(self.url_post_create, 302)

        self.client.force_login(self.user)

        self.assertGetHTTPCode(self.url_post_create, 200)

    def test_post_creation(self):
        self.client.force_login(self.user)
        data = {
            'title': 'Creation test',
            'message': 'Message'
        }

        self.assertPostHTTPCode(self.url_post_create, data, 302)

        Post.objects.get(title=data['title'])

    def test_invalid_post_creation(self):
        self.client.force_login(self.user)
        data = {
            'title': '',
            'message': ''
        }

        self.assertPostHTTPCode(self.url_post_create, data, 200)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(title=data['title'])

# Forms tests
class TestPostForm(TestForum):
    def test_valid_create_form(self):
        form = PostForm(
            data = {
                'title': 'Nice',
                'message': 'Nice',
                'author': self.user
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_create_form(self):
        form = PostForm(
            data = {
                'title': '',
                'message': ''
            }
        )

        self.assertFalse(form.is_valid())
