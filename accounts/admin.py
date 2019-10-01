from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile, History, PersonalHistory

admin.site.register(UserProfile)

admin.site.register(History)

admin.site.register(PersonalHistory)