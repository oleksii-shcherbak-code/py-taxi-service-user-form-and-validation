from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import Driver

LICENSE_REGEX = RegexValidator(
    regex=r"^[A-Z]{3}\d{5}$",
    message="License number "
            "must have 3 uppercase "
            "letters followed by 5 digits."
)


class DriverForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[LICENSE_REGEX]
    )

    class Meta:
        model = Driver
        fields = ["username",
                  "first_name",
                  "last_name",
                  "license_number",
                  "password"
                  ]

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data["password"])
        if commit:
            driver.save()
        return driver


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[LICENSE_REGEX]
    )

    class Meta:
        model = Driver
        fields = ["license_number"]


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
