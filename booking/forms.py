from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Service, TimeSlot


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Nazwa użytkownika",
        }
        help_texts = {
            "username": "Wymagane. Maks. 150 znaków. Litery, cyfry oraz @/./+/-/_",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # bootstrap + placeholdery + polskie etykiety
        for name, field in self.fields.items():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label

        self.fields["password1"].label = "Hasło"
        self.fields["password2"].label = "Powtórz hasło"

        # czytelniejsze help_texty
        self.fields["password1"].help_text = (
            "<ul class='small mb-0'>"
            "<li>Minimum 8 znaków.</li>"
            "<li>Nie może być zbyt podobne do nazwy/emaila.</li>"
            "<li>Nie może być popularnym hasłem.</li>"
            "<li>Nie może składać się tylko z cyfr.</li>"
            "</ul>"
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest już zajęty.")
        return email


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nazwa użytkownika"}
        ),
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Hasło"}
        ),
    )


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["slot"]

    def __init__(self, *args, **kwargs):
        service = kwargs.pop("service", None)
        super().__init__(*args, **kwargs)

        if service:
            self.fields["slot"].queryset = TimeSlot.objects.filter(
                service=service, is_active=True
            ).exclude(reservation__isnull=False)


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class SlotAdminForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["service", "start", "end", "is_active"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
            "start": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
