from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']
        labels = {'username': 'Nombre de Usuario'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['password'].label = 'Contraseña'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": (
                    "w-full border border-gray-300 rounded-lg px-3 py-2 "
                    "focus:outline-none focus:ring-2 focus:ring-blue-500 "
                    "focus:border-blue-500 placeholder-gray-400 text-gray-800"
                ),
                "placeholder": field.label
            })


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {'username': 'Nombre de Usuario'}
        help_texts = {'username': ''}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar Contraseña'
        self.fields["password1"].help_text = ''
        self.fields["password2"].help_text = ''

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": (
                    "w-full border border-gray-300 rounded-lg px-3 py-2 "
                    "focus:outline-none focus:ring-2 focus:ring-blue-500 "
                    "focus:border-blue-500 placeholder-gray-400 text-gray-800"
                ),
                "placeholder": field.label
            })


class UserProfileForm(forms.ModelForm):

    current_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput,
        required=False
    )

    new_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    confirm_password = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {'username': ''}
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['email'].label = 'Correo Electrónico'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": (
                    "w-full border border-gray-300 rounded-lg px-3 py-2 "
                    "focus:outline-none focus:ring-2 focus:ring-blue-500 "
                    "focus:border-blue-500 placeholder-gray-400 text-gray-800"
                ),
                "placeholder": field.label
            })

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError("Debes ingresar tu contraseña actual para cambiarla.")
            if not self.user.check_password(current_password):
                raise forms.ValidationError("La contraseña actual es incorrecta.")
            if new_password != confirm_password:
                raise forms.ValidationError("La nueva contraseña no coincide.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user