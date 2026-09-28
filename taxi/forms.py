from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriversForm(UserCreationForm):

    class Meta:
        model = Driver
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError("Ensure that value is correct length!")

        if not license_number[:3].isupper():
            raise ValidationError(
                "Ensure that value is starts with Uppercase!"
            )

        if not license_number[3:].isnumeric():
            raise ValidationError("Ensure that value is end with digits!")

        return license_number


class DriverLicenseForm(DriversForm):

    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
