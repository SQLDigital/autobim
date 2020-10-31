from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from tidp.models import Task, Project, ProjectTask, TaskLeader, TaskMember


@login_required
def dashboard(request):
    if request.user.is_superuser:
        number_of_projects = Project.objects.all().count()
        number_of_tasks = Task.objects.all().count()
        number_of_due_tasks = ProjectTask.objects.filter().count()
        number_of_midps = 0

        context = {
            'number_of_projects': number_of_projects,
            'number_of_tasks': number_of_tasks,
            'number_of_midps': number_of_midps,
            'number_of_due_tasks': number_of_due_tasks,
        }

        return render(request, 'dashboard.html', context)

    else:
        task_leaders = TaskLeader.objects.filter(user=request.user).values('project')
        task_members = TaskMember.objects.filter(user=request.user).values('project')

        projects_for_leader = Project.objects.filter(id__in=task_leaders)
        projects_for_member = Project.objects.filter(id__in=task_members)

        context = {
            "projects_for_leader": projects_for_leader,
            "projects_for_member": projects_for_member,
        }
        return render(request, 'leader_dashboard.html', context)
