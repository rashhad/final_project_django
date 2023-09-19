from django.db import models
from posts.models import posts
from django.contrib.auth.models import User
# Create your models here.


class interactions(models.Model):
    post=models.ForeignKey(posts, on_delete=models.CASCADE, related_name='interactions')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactor')
    comment=models.TextField()
    rating=models.IntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post','user')
    def __str__(self) -> str:
        return f"{self.user.first_name}-{self.post.title}"

class relpies(models.Model):
    comment=models.ForeignKey(interactions, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replier')
    reply=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.first_name}-{self.comment}"

