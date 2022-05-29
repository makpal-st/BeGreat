from utils.services import get_random_name


def avatar_upload(instance, filename):
    y = get_random_name()
    name, extension = filename.split('.')
    return 'profile_avatar/{}/{}.{}'.format(
        instance.id, y, extension
    )


def create_user(kwargs):
    from autho.models import User
    user = User.objects.create_user(**kwargs)
    return user
