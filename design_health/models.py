from django.db import models
# Create your models here.


class Role(models.Model):
  STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
  ]
  name = models.CharField(max_length=80, unique=True)
  status = models.CharField(max_length=31, choices=STATUS, default="active")
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.name


class Company(models.Model):
  company_name = models.CharField(max_length=80, unique=True)
  street_name = models.CharField(max_length=100, blank=True)
  street_number = models.CharField(max_length=5, blank=True)
  city = models.CharField(max_length=100, blank=True)
  postal_code = models.CharField(max_length=10, blank=True)
  country = models.CharField(max_length=50, blank=True)
  phone_number = models.CharField(max_length=15, blank=True)
  contact_person = models.CharField(max_length=30, blank=True)
  email = models.EmailField()

  def __str__(self):
      return self.company_name


class DesignCategory(models.Model):
  DESIGN_TYPES = (
    ("concept_design", "Concept Design"),
    ("technical_design", "Technical Design"),
    ("developed_design", "Developed Design"),
  )
  name = models.CharField(max_length=200, unique=True)
  design_type = models.CharField(max_length=20, choices=DESIGN_TYPES)

  def __str__(self):
      return self.name


class Task(models.Model):
  STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
  ]

  DESIGN_TYPES = (
      ("concept_design", "Concept Design"),
      ("technical_design", "Technical Design"),
      ("developed_design", "Developed Design"),
  )

  design_type = models.CharField(max_length=25, choices=DESIGN_TYPES)
  design_category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE)
  task_name = models.CharField(max_length=200)
  status = models.CharField(max_length=20, choices=STATUS, default="active")
  default_role = models.ForeignKey(Role, on_delete=models.CASCADE)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.task_name


class Project(models.Model):
  project_name = models.CharField(max_length=80, unique=True)
  project_code = models.CharField(
      max_length=8, unique=True, blank=True)
  further_details_1 = models.CharField(
      max_length=200, blank=True)
  further_details_2 = models.CharField(
      max_length=200, blank=True)
  start_date = models.DateTimeField(blank=True, null=True)
  end_date = models.DateTimeField(blank=True, null=True)
  client = models.ForeignKey(Company, on_delete=models.CASCADE)

  def __str__(self):
      return self.project_name


class ProjectRole(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)


class ProjectTask(models.Model):
  WORK_STATUS = [
    ('pending', 'Pending'),
    ('incomplete','Incomplete'),
    ('çomplete','Complete'),

  ]
  APPROVAL_STATUS = [
    ('pending', 'Pending'),
    ('incomplete','Incomplete'),
    ('approved','Approved/Reviewed'),

  ]
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  work_status = models.CharField(max_length=20, choices=WORK_STATUS)
  approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS)