from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Request, Review

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'fio', 'birth_date', 'phone', 'email', 'password1', 'password2')
        widgets = {
            'birth_date': forms.DateInput(format='%d.%m.%Y', attrs={'type': 'date', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'fio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Латиница и цифры, от 6 символов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('transport', 'start_date', 'payment_method')
        widgets = {
            'start_date': forms.DateInput(format='%d.%m.%Y', attrs={'type': 'date', 'class': 'form-control'}),
            'transport': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш отзыв...'}),
        }