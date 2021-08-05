from django import forms
from .models import CarBooking

class DateInput(forms.DateInput):
    input_type = 'date'

    
class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['returning_date', 'destination']
        widgets = {
            'returning_date': DateInput(),
        }


class RatingForm(forms.Form):
    choices = (('1',1),('2',2),('3',3),('4',4),('5',5))
    rating  = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)