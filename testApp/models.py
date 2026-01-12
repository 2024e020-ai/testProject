from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testapp_posts')

    # いいね機能
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'
