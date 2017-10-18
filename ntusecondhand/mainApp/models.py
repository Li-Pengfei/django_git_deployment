from django.db import models
from django.contrib.auth.models import User


# Authentication User
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!
    user = models.OneToOneField(User)

    # add any additional attributes you want
    wechat = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username


# Item Model
class ItemModel(models.Model):

    CAT_CHOICES = [
        ('EL', 'Electronics'),
        ('FA', 'Fashion & Accessories'),
        ('HA', 'Home & Appliances'),
        ('HB', 'Health & Beauty'),
        ('BT', 'Baby & Toy'),
        ('SO', 'Sports & Outdoors'),
        ('GC', 'Groceries'),
        ('OT', 'Others'),
    ]

    user = models.ForeignKey(User, related_name='items')
    category = models.CharField(max_length=64, choices=CAT_CHOICES)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    estimate_price = models.PositiveIntegerField()
    exchange_address = models.TextField(max_length=256)
    item_pic = models.URLField()

    def __str__(self):
        return str(self.user) + ": " + self.title

    def category_verbose(self):
        return dict(ItemModel.CAT_CHOICES)[self.category]


