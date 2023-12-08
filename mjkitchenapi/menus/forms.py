from django import forms
from django.forms import ModelForm
from .models import Menu


class MenuForm(ModelForm):
    class Meta:
        model = Menu

        fields = '__all__'

        labels = {
            'foodtype': 'foodtype',
            'foodname': 'foodname',
            'foodprice': 'foodprice',
            'foodimage': ''
        }

        widgets = {
            'foodtype': forms.TextInput({'class': 'form-control', 'placeholder': 'food type'}),
            'foodname': forms.TextInput({'class': 'form-control', 'placeholder': 'food name'}),
            'foodprice': forms.TextInput({'class': 'form-control', 'placeholder': 'food price'}),
            'foodimage': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
