from django.db import models
from django.contrib.auth.models import User


# Authentication User
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!
    user = models.OneToOneField(User)

    # add any additional attributes you want
    wechat = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=6)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

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

    CONDITION_CHOICES = [
        ('Used', 'Used'),
        ('New', 'New'),
        ('80', '80% New'),
        ('Obsolete', 'Obsolete',)
    ]

    user = models.ForeignKey(User, related_name='items')
    category = models.CharField(max_length=64, choices=CAT_CHOICES)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    condition = models.CharField(max_length=64, choices=CONDITION_CHOICES, default="Used")
    estimate_price = models.PositiveIntegerField()
    exchange_address = models.TextField(max_length=256)
    item_pic = models.URLField()

    def __str__(self):
        return str(self.user) + ": " + self.title

    def category_verbose(self):
        return dict(ItemModel.CAT_CHOICES)[self.category]


class Offer(models.Model):

    TYPE_CHOICES = [
        ('CS', 'Cash'),
        ('EX', 'Exchange'),
    ]

    STAT_CHOICES = [
        ('ON', 'Active'),
        ('FI', 'Finished'),
        ('CA', 'Canceled'),
    ]

    def status_verbose(self):
        return dict(Offer.STAT_CHOICES)[self.offer_status]

    initiator = models.ForeignKey(ItemModel, related_name='offered', blank=True, null=True)
    receiver = models.ForeignKey(ItemModel, related_name='wanted')

    offer_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    offer_status = models.CharField(max_length=3, choices=STAT_CHOICES)

