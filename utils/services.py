import random
import string


def get_random_name(length=25):
    y = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))
    return y


def images_upload(instance, filename):
    y = get_random_name()
    name, extension = filename.split('.')
    return 'images/{}/{}.{}'.format(
        instance.id, y, extension
    )


def prize_upload(instance, filename):
    y = get_random_name()
    name, extension = filename.split('.')
    return 'prizes/{}/{}.{}'.format(
        instance.id, y, extension
    )


def avatar_upload(instance, filename):
    y = get_random_name()
    name, extension = filename.split('.')
    return 'profile_avatar/{}/{}.{}'.format(
        instance.id, y, extension
    )
