from django.db.models.signals import post_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver

from users.models import User
from .models import Task, TaskLeader, TaskMember, Project, ProjectRole, ProjectTask
from .mailer import task_leader_mail, task_member_mail


@receiver(post_save, sender=Project)
def after_updating(sender, instance, created, **kwargs):
    if not created:
        projectroles = instance.projectrole_set.all()
        projectroles.update(is_active=True)


@receiver(m2m_changed, sender=TaskLeader.roles.through)
def after_adding_leader_to_task(sender, instance, action, **kwargs):
    if action == "post_add":
        task_leader_mail(instance, instance.project.author.email)
        for role in instance.roles.all():
            projectrole, created = ProjectRole.objects.get_or_create(
                project=instance.project,
                role = role,
                company=instance.company,
            )
            tasks = Task.objects.filter(role=role, discipline_category=instance.project.discipline_category)
            projecttasks = []
            for task in tasks:
                itexists = ProjectTask.objects.filter(
                    project_role=projectrole,
                    discipline = task.discipline,
                    discipline_category=task.discipline_category,
                    task_type=task.task_type,
                ).exists()
                if not itexists:
                    projecttasks.append(ProjectTask(
                        project_role=projectrole,
                        description = task.description,
                        discipline = task.discipline,
                        discipline_category=task.discipline_category,
                        task_type=task.task_type,
                        uniclass_code=task.uniclass_code,
                    ))
            ProjectTask.objects.bulk_create(projecttasks)


@receiver(pre_delete, sender=TaskLeader)
def after_leader_is_deleted(sender, instance, **kwargs):
    ProjectRole.objects.filter(role__in=instance.roles.all(), company=instance.company).delete()


@receiver(m2m_changed, sender=TaskMember.roles.through)
def after_adding_task_member(sender, instance, action, **kwargs):
    if action == "post_add":
        task_member_mail(instance)
