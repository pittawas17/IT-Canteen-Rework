from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from accounts.models import UserProfile, History

# Create your models here.


class Shop(models.Model):
    shop_host = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100, default="", blank=True)
    shop_validated = models.BooleanField(null=False, default=False)
    OPEN = "01"
    CLOSE = "02"
    BREAK = "03"
    TYPES = (
        (OPEN, "เปิด"),
        (CLOSE, "ปิด"),
        (BREAK, "พัก")
    )
    T8 = "01"
    T9 = "02"
    T10 = "03"
    T11 = "04"
    T12 = "05"
    T13 = "06"
    T14 = "07"
    T15 = "08"
    T16 = "09"
    T17 = "10"
    T18 = "11"
    T19 = "12"
    TIMES = (
        (T8, "ก่อน 8:00"),
        (T9, "8:00 - 9:00"),
        (T10, "9:00 - 10:00"),
        (T11, "10:00 - 11:00"),
        (T12, "11:00 - 12:00"),
        (T13, "12:00 - 13:00"),
        (T14, "13:00 - 14:00"),
        (T15, "14:00 - 15:00"),
        (T16, "15:00 - 16:00"),
        (T17, "16:00 - 17:00"),
        (T18, "17:00 - 18:00"),
        (T19, "หลัง 18:00"),
    )
    status = models.CharField(max_length=2, choices=TYPES, default='01')
    contact1 = models.TextField(null=True)
    contact2 = models.TextField(null=True)
    open_time = models.CharField(max_length=2, null=True, choices=TIMES)
    close_time = models.CharField(max_length=2, null=True, choices=TIMES)

    def __str__(self):
        return self.shop_name


class Menu(models.Model):
    menu_name = models.CharField(max_length=100, null=False)
    is_daily_menu = models.BooleanField(null=False, default=False)
    description = models.TextField(max_length=200, null=True, blank=True)
    normal_price = models.FloatField(null=True, blank=True)
    special_price = models.FloatField(null=True, blank=True)
    hot_price = models.FloatField(null=True, blank=True)
    cold_price = models.FloatField(null=True, blank=True)
    frappe_price = models.FloatField(null=True, blank=True)
    FOOD = "01"
    DRINK = "02"
    TYPES = (
        (FOOD, 'อาหาร'),
        (DRINK, 'เครื่องดื่ม')
    )
    menu_type = models.CharField(max_length=2, choices=TYPES, default="01")
    menu_image = models.FileField(null=True, blank=True)
    menu_of = models.ForeignKey(Shop, on_delete=models.PROTECT, default='99999')

    def __str__(self):
        return self.menu_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50, null=False, default="some ingredient")
    is_empty = models.BooleanField(default=False)
    ingredient_of = models.ForeignKey(Shop, on_delete=models.PROTECT, default='99999')

    def __str__(self):
        return self.ingredient_name


class ShopQueue(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.PROTECT)
    queue = models.IntegerField(null=False, default=0)
    current_queue = models.IntegerField(null=False, default=0)
    last_queue = models.IntegerField(null=False, default=0)

    def __str__(self):
        return '%s\' Queue' % self.shop


class Order(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False, default=0)

    def __str__(self):
        return '%s\' Order(s)' % self.user


class OrderItem(models.Model):
    queue = models.ForeignKey(ShopQueue, on_delete=models.PROTECT, default='99999')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    special_requirement = models.TextField(max_length=100, null=True, blank=True)
    this_queue = models.IntegerField(null=False, default=999999999)
    wait = models.IntegerField(null=False, default=99999999)
    is_confirmed = models.BooleanField(null=False, default=False)
    price = models.FloatField(null=False, default=0)
    order_datetime = models.DateTimeField(null=True)

    def __str__(self):
        return '%s (%s)' % (self.order, self.menu)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(user=instance)


post_save.connect(create_user_profile, sender=UserProfile)
