from django.conf.urls import url
from django.urls import path
from ordering import views

urlpatterns = [
    path('home/', views.home, name='home'),

    # url for customer
    path('shop_list/', views.select_shop, name='show_shop'),
    path('shop/shop_<int:shop_id>/', views.select_menu, name='selected'),
    path('shop/shop_<int:menu_of>/menu_<int:menu_id>/', views.edit_order, name='edit_order'),
    path('update/queue=<int:queue>/', views.update_order, name='update_order'),
    path('remove/shop=<int:shop>menu=<int:menu_id>queue=<int:queue>/', views.remove_order, name='remove_order'),
    path('order_status/', views.show_order_status, name='order_status'),
    path('order_history/', views.show_order_history, name='order_history'),

    # url for shop
    path('shop_cook/shop=<int:shop>order_item=<int:order_item_id>queue=<int:queue>/', views.start_cook, name='start_cook'),
    path('show_ingredient/', views.show_ingredient, name="show_ingredient"),
    path('create_ingredient/', views.create_ingredient, name="create_ingredient"),
    path('update_ingredient/<int:ingre_id>', views.update_ingredient, name="update_ingredient"),
    path('remove_ingredient/<int:ingre_id>', views.remove_ingredient, name="remove_ingredient"),
    path('shop_menu/', views.show_menu, name="show_menu"),
    path('create_menu/', views.create_menu, name="create_menu"),
    path('update_menu/<int:menu_id>', views.update_menu, name="update_menu"),
    path('remove_menu/<int:menu_id>', views.remove_menu, name="remove_menu"),
    path('edit_status/status<int:status>', views.edit_status, name="edit_status")
]