from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)
    likeCount = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag')
    is_private = models.BooleanField(default=False)
    tag = models.TextField(default='影评')

    def __str__(self):
        #return self.title
        comment_count = Comment.objects.filter(post=self).count()
        return f"{self.title} ({comment_count} comments)"

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    # 其他评论相关的字段

    def __str__(self):
        return f"Comment on {self.post.title}"

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_post_comments_count(sender, instance, **kwargs):
    post = instance.post
    comment_count = Comment.objects.filter(post=post).count()
    post.comments = comment_count
    post.save()


class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', related_name='received_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

class Contact(models.Model):
    main_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', related_name='contacts')
    contacted_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)

class WebSocketConnection(models.Model):
    receiver_id = models.IntegerField(unique=True)
    connection_id = models.CharField(max_length=255)
    # 可根据需求添加其他字段

    def __str__(self):
        return f"Receiver ID: {self.receiver_id}, Connection ID: {self.connection_id}"

class UserPublicKey(models.Model):
    user = models.CharField(max_length=255)
    public_key = models.TextField()
    private_key = models.TextField(default='DEFAULT_PRIVATE_KEY_VALUE')

    def __str__(self):
        return self.user

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VerificationCode: {self.code} for {self.user.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def username(self):
        return self.user.username