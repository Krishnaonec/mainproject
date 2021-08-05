from datetime import date, timedelta
from django.core.exceptions import ValidationError

def is_future_date(value):
    if value < date.today() + timedelta(days = 1) :
        raise ValidationError("The date should be in future")
    else:
        return value