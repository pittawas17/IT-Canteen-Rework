from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import ModelForm

from accounts.models import UserProfile
from ordering.models import Shop, OrderItem, Ingredient, Menu


class EditOrderModelForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['special_requirement']


class IngredientModelForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name', 'is_empty']


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_name', 'is_daily_menu', 'description', 'normal_price', 'special_price', 'menu_type', 'menu_image', 'hot_price', 'cold_price', 'frappe_price']
        # help_texts = {
        #     'special_price': '<p style="color: red">กำหนดหรือไม่ก็ได้</p>'
        # }

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('menu_type')
        normal = cleaned_data.get('normal_price')
        special = cleaned_data.get('special_price')
        hot = cleaned_data.get('hot_price')
        cold = cleaned_data.get('cold_price')
        frappe = cleaned_data.get('frappe_price')

        if type == "01":
            if not normal:
                self.add_error('normal_price', 'please set your menu price')
            elif hot:
                self.add_error('hot_price', 'FOOD has no hot type price, please don\'t fill this field')
            elif cold:
                self.add_error('cold_price', 'FOOD has no cold type price, please don\'t fill this field')
            elif frappe:
                self.add_error('frappe_price', 'FOOD has no frappe type price, please don\'t fill this field')

        elif type == "02":
            if not hot and not cold and not frappe:
                self.add_error('hot_price', 'please set your menu price at least 1 of 3')
                self.add_error('cold_price', 'please set your menu price at least 1 of 3')
                self.add_error('frappe_price', 'please set your menu price at least 1 of 3')
            elif normal:
                self.add_error('normal_price', 'DRINK has no normal type price, please don\'t fill this field')
            elif special:
                self.add_error('special_price', 'DRINK has no special type price, please don\'t fill this field')
