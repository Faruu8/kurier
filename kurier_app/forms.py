from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Customer, Package, CustomerLocation, Recipient, Courier

from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    address = forms.CharField(max_length=100)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nazwa użytkownika jest już zajęta.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Hasła nie są identyczne.")

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['weight', 'description']


class CustomerLocationForm(forms.ModelForm):
    class Meta:
        model = CustomerLocation
        fields = ['address', 'city', 'postal_code']

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'address', 'city', 'postal_code']

class CourierRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_courier = True
        user.save()
        phone = self.cleaned_data['phone']
        Courier.objects.create(user=user, phone=phone)
        return user

class CourierLoginForm(AuthenticationForm):
    phone = forms.CharField(max_length=15)


