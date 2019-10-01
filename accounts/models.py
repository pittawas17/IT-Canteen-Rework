from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.TextField(max_length=10, null=True)
    email = models.TextField(null=True)
    register_date_time = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    real_first_name = models.TextField(null=True)
    real_last_name = models.TextField(null=True)
    CUSTOMER = "01"
    SHOP = "02"
    TYPES = (
        (CUSTOMER, 'customer'),
        (SHOP, 'shop')
    )
    type = models.CharField(max_length=2, choices=TYPES, default='01')

    def __str__(self):
        return '%s %s' % (self.real_first_name, self.real_last_name)


class History(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.PROTECT)
    total_price = models.FloatField(null=False, default=0)

    def __str__(self):
        return '%s\'s Order History' % self.user


class PersonalHistory(models.Model):
    history = models.ForeignKey(History, on_delete=models.PROTECT)
    menu = models.TextField(null=False, default='some menu')
    shop = models.TextField(null=False, default='some shop')
    order_datetime = models.DateTimeField(null=True)
    price = models.FloatField(null=False,default=0)

    def __str__(self):
        return '%s\' Order History (Detail)' % (self.history.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        History.objects.create(user=instance.userprofile)


post_save.connect(create_user_profile, sender=User)
