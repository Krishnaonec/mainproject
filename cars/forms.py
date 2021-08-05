from django.core.validators import FileExtensionValidator
from django import forms 
from .models import UserCar
from validators import validate_image

class RegisterCarForm(forms.ModelForm):
    image = forms.ImageField(
                        widget=forms.FileInput, 
                        required=True, 
                        validators=[validate_image, FileExtensionValidator(allowed_extensions=['jpg','png'])])
    class Meta:
        model  = UserCar
        fields = ['carbrand','carmodel','price','image']