from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post

class TestForum(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('Bob')
        self.superuser = User.objects.create_superuser('root')

        self.post = Post.objects.create(
            author = self.user,
            title = 'test',
            message = 'This is a test message to test things out'
        )

class TestTemplates(TestForum):
    def http_code_test(self, url, code=200):
        return self.assertEqual(self.client.get(url).status_code, code)

    def test_templates(self):
        url_post_list = reverse('forum:post-list')
        url_post_create = reverse('forum:post-create')
        url_post_detail = reverse('forum:post-detail', args=[self.post.id])

        self.http_code_test(url_post_list, 200)
        self.http_code_test(url_post_detail, 200)
        self.http_code_test(url_post_create, 302)

        self.client.force_login(self.user)

        self.http_code_test(url_post_create, 200)
