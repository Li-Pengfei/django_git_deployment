from django.db import models
from django.contrib.auth.models import User


# Authentication User
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!
    user = models.OneToOneField(User)

    # add any additional attributes you want
    wechat = models.CharField(max_length=128)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
