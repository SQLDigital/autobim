from django import forms

from .models import Company, DesignCategory, Role, Task, Project, ProjectRole, ProjectTask

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        companies = Company.objects.filter(company_name=company_name).exists()
        if companies:
            raise forms.ValidationError("Company name already exists!")

        return company_name


class DesignCategoryForm(forms.ModelForm):
    class Meta:
        model = DesignCategory
        fields = ['name', 'design_type']
        widgets = {
            "name": forms.TextInput(attrs={"placeholder":"Enter a new category"})
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        design = DesignCategory.objects.filter(name=name).exists()
        if design:
            raise forms.ValidationError("Design name already exists!")

        return name


class SearchDesignCategory(forms.Form):
    CHOICES = [
        ('', '----'),
        ('concept_design', 'Concept Design'),
        ('developed_design', 'Developed Design'),
        ('technical_design', 'Technical Design'),
    ]
    category = forms.ChoiceField(
        choices=CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"}),
        label = 'Search by category',
        )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('design_type',)
    
    def __init__(self, dtype, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['design_category'].queryset = DesignCategory.objects.filter(design_type=dtype)
    


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ()
        labels = {
            "project_name": "Create a new project title (Maximum of 200 characters)",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={'type':'date'}),
            "end_date": forms.DateInput(attrs={'type':'date'}),
            "client": forms.Select(attrs={'class': "searchable"}),
        }


class SearchProject(forms.Form):
    project = forms.CharField(max_length=200, label="Search for a project", required=False)
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), 
        required=False,
        widget=forms.Select(attrs={"class":"searchable"})
    )


class EditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']


class ProjectRoleFormBase(forms.ModelForm):
    class Meta:
        model = ProjectRole
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(ProjectRoleFormBase, self).__init__(*args, **kwargs)
        self.fields['company'].empty_label = "N/A"

ProjectRoleForm = forms.inlineformset_factory(
    Project,
    ProjectRole,
    exclude=('project',),
    can_delete=False,
    widgets={
        "role": forms.Select(attrs={"readonly":True, "hidden":True,}),
    },
    form=ProjectRoleFormBase,
    
)

ProjectTaskForm = forms.inlineformset_factory(
    Project,
    ProjectTask,
    exclude=('project',),
    can_delete=False,
    widgets={
        "task": forms.Select(attrs={"readonly":True, "hidden":True,}),
    }
)