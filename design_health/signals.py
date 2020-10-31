from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Role, Project, ProjectRole

@receiver(post_save, sender=Project)
def add_client_after_saving_new_project(sender, created, instance, *args, **kwargs):
    if created:
        company = instance.client
        role, created = Role.objects.get_or_create(name='Client')
        ProjectRole.objects.create(project=instance, role=role, company=company)
        
