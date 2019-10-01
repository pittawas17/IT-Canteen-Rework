from django.conf.urls import url
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.login_success, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]