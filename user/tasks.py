from user.models import UsersPassword
from celery import shared_task

@shared_task
def delete_passwords():
    UsersPassword.objects.all().delete()
    return 'All passwords have been deleted!'