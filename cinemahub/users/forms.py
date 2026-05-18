from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=50, required=True, label="Ism")
    last_name = forms.CharField(max_length=50, required=True, label="Familiya")
    phone = forms.CharField(max_length=20, required=False, label="Telefon")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        self.fields['username'].label = "Foydalanuvchi nomi"
        self.fields['password1'].label = "Parol"
        self.fields['password2'].label = "Parolni tasdiqlash"


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        self.fields['username'].label = "Foydalanuvchi nomi"
        self.fields['password'].label = "Parol"


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-input'})
