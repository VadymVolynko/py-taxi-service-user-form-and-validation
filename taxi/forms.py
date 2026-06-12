import re

from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    """Form for creating a new Driver with license validation."""

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self) -> str:
        """Validate the license number format."""
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    """Form for updating driver's license number."""

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        """Validate the license number format."""
        return validate_license_number(
            self.cleaned_data["license_number"]
        )


def validate_license_number(license_number: str) -> str:
    """Check license: 3 uppercase letters + 5 digits, total 8 chars."""
    if len(license_number) != 8:
        raise forms.ValidationError(
            "License number must consist of exactly 8 characters."
        )
    if not re.match(r"^[A-Z]{3}\d{5}$", license_number):
        raise forms.ValidationError(
            "License number must start with 3 uppercase letters "
            "followed by 5 digits."
        )
    return license_number
