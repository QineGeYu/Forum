from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# # Create your models here.
# user1 = User.objects.create_user(username=123,password=123)
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)
    likeCount = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name