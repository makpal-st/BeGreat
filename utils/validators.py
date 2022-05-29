from rest_framework.exceptions import ValidationError


def validate_image(file):
    name, extension = file.name.split('.')
    if not extension.lower().endswith(('png', 'jpg', 'jpeg', 'svg')):
        raise ValidationError('File is not an image')


def validate_pdf(file):
    name, extension = file.name.split('.')
    if not extension.lower().endswith(('pdf',)):
        raise ValidationError('File is not an pdf')
