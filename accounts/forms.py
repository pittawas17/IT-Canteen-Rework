from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import ModelForm

from accounts.models import UserProfile
from ordering.models import Shop


class RegisterForm(forms.Form):
    real_first_name = forms.CharField(label="First Name", required=True)
    real_last_name = forms.CharField(label="Last Name", required=True)
    phone_number = forms.CharField(label="Phone Number", max_length=10, required=True)
    email = forms.CharField(label="E-mail", validators=[validators.validate_email], required=True, help_text=' * ใส่ \
E-mail ที่ท่านมั่นใจว่าจะเห็นแจ้งเตือนได้ทันทีที่ได้รับเมลล์แจ้งเตือนจากเรา โดยไม่จำเป็นต้องเป็น E-mail เดียวกับที่ใช้ log in')

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone_number')
        first_name = cleaned_data.get('real_first_name')
        last_name = cleaned_data.get('real_last_name')

        if first_name is not None:
            for a in first_name:
                if not a.isalpha():
                    self.add_error('real_first_name', 'กรุณาตรวจสอบว่าใส่ชื่อถูกต้อง')
                    break

        if last_name is not None:
            for b in last_name:
                if not b.isalpha():
                    self.add_error('real_last_name', 'กรุณาตรวจสอบว่าใส่นามสกุลถูกต้อง')
                    break

        if len(phone) != 10:
            self.add_error('phone_number', 'กรุณาใส่เบอร์ให้ถูกต้อง')
        else:
            for c in phone:
                if not c.isdigit():
                    self.add_error('real_last_name', 'กรุณาใส่เบอร์ให้ถูกต้อง')
                    break


class ShopModelForm(forms.ModelForm):
    real_first_name = forms.CharField(label="First Name", required=True)
    real_last_name = forms.CharField(label="Last Name", required=True)
    phone_number = forms.CharField(label="Phone Number", max_length=10, required=True)
    email = forms.CharField(label="E-mail", validators=[validators.validate_email], required=True, help_text=' * ใส่ \
E-mail ที่ท่านมั่นใจว่าจะเห็นแจ้งเตือนได้ทันทีที่ได้รับเมลล์แจ้งเตือนจากเรา โดยไม่จำเป็นต้องเป็น E-mail เดียวกับที่ใช้ log in')

    class Meta:
        model = Shop
        exclude = ['shop_host', 'shop_validated', 'status']
        fields = ['real_first_name', 'real_last_name', 'phone_number', 'email', 'shop_name', 'contact1', 'contact2', 'open_time', 'close_time']

        labels = {
            'shop_name': 'Shop name',
            'contact1': 'Contact 1',
            'contact2': 'Contact 2',
            'open_time': 'Opening time',
            'close_time': 'Closing time'
        }

