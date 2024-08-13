from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name","image"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"placeholder":"Category Name","class":"form-control"}),
            "image":forms.widgets.FileInput(attrs={"class":"form-control"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "description","image"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"placeholder":"Product Name","class":"form-control"}),
            "category":forms.widgets.Select(attrs={"class":"form-control"}),
            "price":forms.widgets.NumberInput(attrs={"placeholder":"Product Price","class":"form-control"}),
            "description":forms.widgets.Textarea(attrs={"placeholder":"Product Description","class":"form-control"}),
            "image":forms.widgets.FileInput(attrs={"class":"form-control"}),
        }
