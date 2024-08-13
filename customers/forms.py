from django import forms

from .models import Order
from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","password","email","phone_number"]

        widgets = {
            "first_name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Full name"}),
            "username":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Username"}),
            "phone_number":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Phone Number"}),
            "password":forms.widgets.PasswordInput(attrs={"class": "form-control","placeholder":"Password"}),
            "email":forms.widgets.EmailInput(attrs={"class": "form-control","placeholder":"Email"}),
        }



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["address","pincode"]

        widgets = {
            "address":forms.widgets.Textarea(attrs={"placeholder":"Address", "class": "border rounded-xl block w-full mb-4 py-2 px-5"}),
            "pincode":forms.widgets.NumberInput(attrs={"placeholder":"pincode", "class": "border rounded-xl block w-full mb-4 py-2 px-5"}),
        }