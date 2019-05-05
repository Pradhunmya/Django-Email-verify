from django import forms
from PIL import Image
from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'ENter passsword'}))
    email = forms.EmailField(max_length=200, help_text='Required')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm passsword'}))
    class Meta:

        model = User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError('Password Mismatch')
        return confirm_password


class ImageForm(forms.Form):
    f_image = forms.ImageField()