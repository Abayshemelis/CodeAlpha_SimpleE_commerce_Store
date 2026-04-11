from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Standard Login Form - Clean and simple
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

# Registration Form
class ExtendedRegistrationForm(UserCreationForm):
    # email is built into User, so we just customize the widget
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        required=True
    )
    
    # These two are EXTRA fields (not in the default User model)
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number (e.g. +251...)'}),
        required=False # Set to False if you haven't created a Profile model yet
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False,
        label="Date of Birth"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Only include fields that actually exist in the User model here
        fields = UserCreationForm.Meta.fields + ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excellent: This loop ensures all fields look great with your CSS
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})