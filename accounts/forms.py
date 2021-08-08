from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from validators import validate_image
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = "Webex email is recommended"
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        emails = User.objects.filter(email=self.cleaned_data['email'])
        if emails:
            raise ValidationError("Email already exists")
        return self.cleaned_data['email']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
    def clean_email(self):
        emails = User.objects.filter(email= self.cleaned_data['email'])
        if (emails.count() == 1 and emails[0].username == self.cleaned_data['username']) or emails.count() == 0:
            return self.cleaned_data['email']
        else:
            raise ValidationError("Email already exists!")


class ProfileUpdateForm(forms.ModelForm):
    cities = [('Chennai', 'Chennai'), ('Hyderabad', 'Hyderabad'), ('Bengauluru', 'Bengaluru')]
    city = forms.ChoiceField(choices= cities, required=False)
    profile_pic = forms.ImageField(
                        widget=forms.FileInput,
                        required=False, 
                        validators=[validate_image,FileExtensionValidator(allowed_extensions=['jpg','png', 'jpeg'])])
    
    class Meta:
        model = Profile
        fields = ['city','profile_pic']