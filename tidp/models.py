import re
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.conf import settings

from .utils import TASK_CHOICES, CATEGORY_CHOICES


class Company(models.Model):
    company_name = models.CharField(max_length=80, unique=True)
    street_number = models.CharField(max_length=5, blank=True)
    street_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    contact_person = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    originator_code = models.CharField(max_length=6, default="ZZ")

    def __str__(self):
        return self.company_name

    @property
    def full_address(self):
        return f'{self.street_number}, {self.street_name}, {self.city}, {self.postal_code}, {self.country}'

class Discipline(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


class DisciplineCategory(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['discipline', 'category'], name='unique_category')
        ]

    def __str__(self):
        return f'{self.discipline} - {self.category}'


class Role(models.Model):
  STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
  ]
  name = models.CharField(max_length=80, unique=True)
  code = models.CharField(max_length=200, blank=True)
  status = models.CharField(max_length=31, choices=STATUS, default="active")
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f'{self.name}'


class TaskType(models.Model):
    title = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Task(models.Model):
    description = models.CharField(verbose_name="Task Title", max_length=100)
    uniclass_code = models.CharField(max_length=20, blank=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    discipline_category = models.ForeignKey(DisciplineCategory, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, verbose_name='Task type/form of information')

    def __str__(self):
        return self.description

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['description', 'discipline', 'discipline_category', 'role', 'task_type'], name='unique_task')
        ]


class ProjectScale(models.Model):
    scale = models.IntegerField()

    def __str__(self):
        return f'{self.scale}'



class Project(models.Model):
    TEMPLATES = [
        ('standard_template', 'Standard Template'),
        ('scottish_template', 'Scottish Template'),
        ('balfour_beatty_template', 'Balfour Beatty Template'),
    ]
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name="tipd_project_client")
    number = models.CharField(max_length=10, blank=True)
    code = models.CharField(max_length=6)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    discipline_category = models.ForeignKey(DisciplineCategory, on_delete=models.CASCADE)
    midp_tipd_template = models.CharField(verbose_name='MIDP/TIDP Template', max_length=50, choices=TEMPLATES, default='standard_template')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('tidp:project-detail', kwargs={'pk': self.pk})


class TaskLeader(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, verbose_name='Company/Originator', null=True)
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField()
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return f'Task leader {self.contact_person}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_leader')
        ]


class TaskMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name='Company/Originator')
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField()
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return f'Task member for {self.project}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_member')
        ]


class ProjectRole(models.Model):
    STATUSES = [
        ('not_sent', 'Not Sent'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    status = models.CharField(choices=STATUSES, max_length=20, default='not_sent')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.role.name} - {self.company.company_name}'


class ProjectTask(models.Model):
    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="Task Title", max_length=100)
    uniclass_code = models.CharField(max_length=20, blank=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    discipline_category = models.ForeignKey(DisciplineCategory, on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, verbose_name='Task type/form of information')
    volume = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=100, blank=True)
    task_category = models.CharField(max_length=100, blank=True)
    exchange_formats = models.CharField(max_length=100, blank=True)
    scale_or_size = models.ForeignKey(ProjectScale, on_delete=models.SET_NULL, null=True, verbose_name='Scale/Size', blank=True)
    eir_reference = models.CharField(verbose_name='EIR Reference', max_length=100, blank=True)
    pir_reference = models.CharField(verbose_name='PIR Reference', max_length=100, blank=True)
    air_reference = models.CharField(verbose_name='AIR Reference', max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    estimated_production_duration = models.CharField(max_length=100, blank=True)
    code = models.IntegerField(editable=False, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['task_type']


    def __str__(self):
        return f'{self.description}'

    @property
    def get_role(self):
        mymatch = re.search(r'\((.+)\)', self.project_role.role.name)
        mrole = mymatch.group(1) if mymatch else '-'
        return mrole

    @property
    def get_tasktype(self):
        mymatch = re.search(r'\((.+)\)', self.task_type.title)
        mdiscipline = mymatch.group(1) if mymatch else '-'
        return mdiscipline

    @property
    def unique_code(self):
        if self.project_role.is_active:
            return '-'
        else:
            number = format(self.code, '05d')
            return f'{self.project_role.project.code}-{self.project_role.project.client.originator_code}-{self.volume}-{self.level}-{self.get_tasktype}-{self.get_role}-{number}'


