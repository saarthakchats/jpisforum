from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    votes_total = models.IntegerField(default=0)
    pubdate = models.DateTimeField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    upvoted_users = models.TextField(default='')
    post_approved = models.BooleanField(default=False)
    post_considered =  models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def preview(self):
        return self.body[:150]
    def pretty_date(self):
        return self.pubdate.strftime('%b %e, %Y')
