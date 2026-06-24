from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
   
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Use at least 8 characters with a mix of letters and numbers.")
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput,
        help_text=_("Use at least 8 characters with a mix of letters and numbers that matches the previous one.")
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'country', 'state', 'address', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")

        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email address already exists."))

        if password and confirm_password and password != confirm_password:
            raise ValidationError(_("Passwords do not match."))
        return cleaned_data

    def save(self, commit=True):
        """Ensures the password is encrypted correctly using set_password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user