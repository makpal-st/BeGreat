import random
import string

from rest_framework.exceptions import ValidationError


def get_random_name(length=25):
    y = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))
    return y


def validate_image(file):
    name, extension = file.name.split('.')
    if not extension.lower().endswith(('png', 'jpg', 'jpeg', 'svg')):
        raise ValidationError('File is not an image')
