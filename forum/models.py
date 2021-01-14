from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Post(models.Model):
	author = models.ForeignKey(
		User,
		on_delete = models.CASCADE
	)
	title = models.CharField(max_length=30)
	message = models.TextField(blank=True)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('forum:post-detail', args=(self.id,))
