from django.db.models.signals import post_save
from django.dispatch import receiver

from autho.models import User, Account


@receiver(post_save, sender=User)
def post_save_user(sender, instance: User, **kwargs):
    if kwargs['created']:
        Account.objects.create(user=instance)
