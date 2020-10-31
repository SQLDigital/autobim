from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django.core.validators import FileExtensionValidator
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Role, Discipline, Task, Project, TaskLeader, Company, TaskMember, TaskType, DisciplineCategory, ProjectTask, ProjectRole, ProjectScale


class DisciplineForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Discipline
        fields = ['name']


class DisciplineCategoryForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = DisciplineCategory
        exclude = ()


class DisciplineSearchForm(forms.Form):
    name = forms.CharField(required=False)


class CompanyForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Company
        fields = '__all__'


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Role
        fields = ['name', 'code']


class RoleFormPopup(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Role
        fields = ['name', 'code']


class TaskForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Task
        exclude = ('is_active',)


class TaskTypeForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = TaskType
        exclude = ()


class TaskSearchForm(forms.Form):
    discipline = forms.ModelChoiceField(Discipline.objects.all(), required=False, widget=forms.Select(attrs={"class":"searchable"}))
    discipline_category = forms.ModelChoiceField(DisciplineCategory.objects.all(), required=False, widget=forms.Select(attrs={"class":"searchable"}))
    role = forms.ModelChoiceField(Role.objects.all(), required=False, widget=forms.Select(attrs={"class":"searchable"}))


class SearchProject(forms.Form):
    name__icontains = forms.CharField(
        max_length=200,
        label="Search for a project",
        required=False,
    )
    client = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class":"searchable"}),
        label='Company'
    )


class ProjectForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'client':
                field.widget.attrs['class'] = 'form-control form-control-sm'
            else:
                field.widget.attrs['class'] = 'form-control searchable'

    class Meta:
        model = Project
        exclude = ('author',)


class ProjectTaskForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = ProjectTask
        fields = ('description', 'uniclass_code', 'task_type')


class TaskLeaderForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['company', 'roles'] :
                field.widget.attrs['class'] = 'searchable form-control form-control-sm'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = TaskLeader
        exclude = ('project', 'user')



class TaskMemberForm(BSModalModelForm):
    def __init__(self, roles=None, *args, **kwargs):
        project = kwargs.pop('project')
        super(TaskMemberForm, self).__init__(*args, **kwargs)
        leader = TaskLeader.objects.filter(user=self.request.user, project=project).first()
        if leader:
            self.fields['roles'].queryset = leader.roles.all()
        for field_name, field in self.fields.items():
            if field_name in ['company', 'roles'] :
                field.widget.attrs['class'] = 'searchable'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = TaskMember
        exclude = ('project','company', 'user')


class Importer(forms.Form):
    header = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
    )
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'accept':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                'class': 'custom-file-input',
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])],
    )


class ImportTaskForm(forms.Form):
    discipline = forms.ModelChoiceField(Discipline.objects.all(), required=False, widget=forms.Select(attrs={"class":"searchable form-control"}))
    discipline_category = forms.ModelChoiceField(DisciplineCategory.objects.all(), required=False, widget=forms.Select(attrs={"class":"searchable form-control"}))
    header = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
    )
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'accept':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                'class': 'custom-file-input',
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])],
    )


class ImportProjectTaskForm(forms.Form):
    header = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class":"form-check-input"}),
    )
    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'accept':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                'class': 'custom-file-input',
            }
        ),
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])],
    )


class StandardTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    CHOICES = [
        ('Models', 'MODELS'),
        ('Drawings', 'DRAWINGS'),
        ('Reports', 'REPORTS'),
        ('Specifications', 'SPECIFICATIONS'),
        ('Others', 'OTHERS'),
    ]

    task_category = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = ProjectTask
        fields = ('volume', 'level', 'exchange_formats', 'task_category')


class ScottishTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    CHOICES = [
        ('Project information', 'Project information'),
        ('Site, ground and environmental information', 'Site, ground and environmental information'),
        ('Project performance requirements', 'Project performance requirements'),
        ('Design and approvals information', 'Design and approvals information'),
        ('Financial and commercial information', 'Financial and commercial information'),
        ('Contract information', 'Contract information'),
        ('Construction management information', 'Construction management information'),
        ('Testing, Commissioning and completion information', 'Testing, Commissioning and completion information'),
        ('Asset management information', 'Asset management information'),
    ]

    task_category = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = ProjectTask
        fields = ('uniclass_code', 'scale_or_size', 'eir_reference', 'pir_reference', 'air_reference', 'task_category')


class BalfourBeattyTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = ProjectTask
        fields = ('volume', 'location', 'estimated_production_duration', 'uniclass_code')


CompleteTasks = modelformset_factory(ProjectTask, fields=(), extra=0)



class ProjectTaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'clone':
                field.widget.attrs['class'] = 'form-control'


    clone = forms.ChoiceField( label="Make multiple copies of x numbers", choices=[('yes', 'Yes'), ('no', 'No')], widget=forms.RadioSelect())
    clone_count = forms.IntegerField(min_value=1, initial=2, label="Number of duplicates", required=False)

    class Meta:
        model = ProjectTask
        fields = ['description', 'uniclass_code', 'task_type', 'clone', 'clone_count']


DuplicateCreateForm = modelformset_factory(ProjectTask, fields = ['description', 'uniclass_code', 'task_type'])


class ProjectScaleForm(forms.ModelForm):
    class Meta:
        model = ProjectScale
        fields = ['scale']


class RoleStatusForm(forms.ModelForm):
    STATUSES = [
        ('pending', 'Pending'),
        ('approved', 'Admit into MIDP'),
        ('rejected', 'Return to task leader'),
    ]
    status = forms.ChoiceField(choices=STATUSES)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = ProjectRole
        fields = ['status', 'comment']
