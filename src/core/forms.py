from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from .models import Pet


class StyledFormMixin:
    def apply_styles(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": (
                    "w-full border border-[#C98259] rounded-lg px-3 py-2 "
                    "focus:outline-none focus:ring-2 focus:ring-[#C98259] "
                    "focus:border-[#B97249] placeholder-gray-400 text-gray-800 "
                    "transition duration-200 "
                )
            })


class BaseStyledForm(forms.Form, StyledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class BaseStyledModelForm(forms.ModelForm, StyledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()


class CustomAuthenticationForm(BaseStyledForm, AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ["username", "password"]
        labels = {"username": "Nombre de Usuario"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nombre de Usuario"
        self.fields["username"].widget.attrs["placeholder"] = "ej: PetLover"
        self.fields["password"].label = "Contraseña"


class CustomCreationForm(BaseStyledForm, UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {"username": "Nombre de Usuario"}
        help_texts = {"username": ""}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "ej: PetLover"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar Contraseña"
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""


class UserProfileForm(BaseStyledModelForm):

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
        fields = ["username", "email"]
        help_texts = {"username": ""}
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nombre de Usuario"
        self.fields["username"].widget.attrs["placeholder"] = "ej: PetLover"
        self.fields["email"].label = "Correo Electrónico"
        self.fields["email"].widget.attrs["placeholder"] = "ej: petlover456@correo.com"

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


class PetForm(BaseStyledModelForm):
    class Meta:
        model = Pet
        fields = [
            "name",
            "age",
            "breed",
            "gender",
            "size",
            "annotations",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={
                "min": 0,
                "max": 99
            }),
            "size": forms.NumberInput(attrs={
                "class": "form-input",
                "step": "0.01"
            }),
            "annotations": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 4
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Nombre"
        self.fields["age"].label = "Edad"
        self.fields["breed"].label = "Raza"
        self.fields["gender"].label = "Género"
        self.fields["size"].label = "Tamaño (kg)"
        self.fields["annotations"].label = "Anotaciones"
        self.fields["name"].widget.attrs["placeholder"] = "Ej: Max, Copito, Zeus"
        self.fields["size"].widget.attrs["placeholder"] = "Ej: 12.5"
        self.fields["annotations"].widget.attrs["placeholder"] = "Ej: Alergias, comportamiento, medicación, etc."

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and age < 0:
            raise forms.ValidationError("La edad debe ser mayor que 0.")
        return age

    def clean_size(self):
        size = self.cleaned_data.get("size")
        if size is not None and size <= 0:
            raise forms.ValidationError("El tamaño debe ser mayor que 0.")
        return size