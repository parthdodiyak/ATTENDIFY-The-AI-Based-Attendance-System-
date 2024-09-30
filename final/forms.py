from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)  # Email field marked as required
    password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
