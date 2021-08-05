from django.core.exceptions import ValidationError

def validate_image(value):
    print(value.content_type)
    if value.size > 1 * 1024 * 1024:
        raise ValidationError("Size too large! Max. allowed size is 1MB")
    else:
        return value