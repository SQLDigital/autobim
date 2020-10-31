from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse


from .models import Role, Company, Project, DesignCategory, Task, ProjectRole, ProjectTask
from .forms import CompanyForm, DesignCategoryForm, RoleForm, TaskForm, ProjectForm, SearchProject, EditForm, ProjectRoleForm, ProjectTaskForm, SearchDesignCategory


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.id,
            }
            return JsonResponse(data)
        else:
            return response


def role_list_view(request):
  if request.method == 'POST':
    form = RoleForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(request.path)
  else:
    form = RoleForm()

  role_list = Role.objects.all()
  paginator = Paginator(role_list, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    "form": form,
    "page_obj": page_obj,
  }

  return render(request, 'design_health/roles.html', context)


class RoleUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Role
    fields = ['name', 'status']
    success_message = 'Role successfully updated.'
    success_url = reverse_lazy('design-roles')

    def test_func(self):
      return self.request.user.is_superuser


class RoleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Role
    template_name = "design_health/delete_form.html"
    success_url = reverse_lazy('design-roles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Role Delete"
        return context

    def test_func(self):
      return self.request.user.is_superuser



class CompanyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Company
    template_name = "design_health/company_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_form'] = CompanyForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class CompanyCreateView(LoginRequiredMixin, UserPassesTestMixin, AjaxableResponseMixin, SuccessMessageMixin, CreateView):
    model = Company
    fields = '__all__'
    template_name = 'design_health/new_company.html'
    success_message = 'New company added'
    success_url = reverse_lazy('company-list')

    def test_func(self):
        return self.request.user.is_superuser


class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Company
    fields = '__all__'
    template_name = 'design_health/edit_company.html'
    success_message = 'Company has been Updated Successfully'
    success_url = reverse_lazy('company-list')

    def test_func(self):
        return self.request.user.is_superuser


class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    template_name = 'design_health/delete_form.html'
    success_url = reverse_lazy('company-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Company Delete"
        return context

    def test_func(self):
        return self.request.user.is_superuser

@login_required()
def design_categories_view(request):
  form = DesignCategoryForm()
  search = SearchDesignCategory(initial={"category":request.GET.get('category')})
  categories = DesignCategory.objects.none()
  if request.GET.get('category'):
    categories = DesignCategory.objects.filter(design_type=request.GET.get('category'))

  if request.method == 'POST':
    form = DesignCategoryForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'New category added.')
      return redirect(request.path)

  

  context = {
    "form": form,
    "search": search,
    "page_obj": categories,
  }

  return render(request, "design_health/designcategory_list.html", context)


class DesignCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = DesignCategory
    fields = ['name', 'design_type']
    template_name = 'design_health/edit_designcategory.html'
    success_message = 'Design Category has been Updated Successfully'
    success_url = reverse_lazy('design-categories')

    def test_func(self):
        return self.request.user.is_superuser


class DesignCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DesignCategory
    template_name = 'design_health/delete_form.html'
    success_url = reverse_lazy('design-categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Design Categohhhhhhry"
        return context

    def test_func(self):
        return self.request.user.is_superuser


@login_required()
def concept_design_view(request):
  categories = DesignCategory.objects.all()
  tasks = Task.objects.filter(design_type='concept_design')
  new_data = {}
  for category in categories:
    new_data[category.name] = []
    for task in tasks:
      if task.design_category == category:
        new_data[category.name].append(task)

  if request.method == 'POST':
    form = TaskForm('concept_design', request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.design_type = 'concept_design'
      form.save()
      messages.success(request, 'Task successfully added.')
      return redirect(request.path)
  else:
    form = TaskForm(dtype='concept_design')

  context = {
    "obj_list": new_data,
    "form": form,
    "title": 'Concept Design',
  }
  return render(request, "design_health/design_task_list.html", context)


@login_required()
def technical_design_view(request):
  categories = DesignCategory.objects.all()
  tasks = Task.objects.filter(design_type='technical_design')
  new_data = {}
  for category in categories:
    new_data[category.name] = []
    for task in tasks:
      if task.design_category == category:
        new_data[category.name].append(task)

  if request.method == 'POST':
    form = TaskForm('technical_design', request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.design_type = 'technical_design'
      form.save()
      messages.success(request, 'Task successfully added.')
      return redirect(request.path)
  else:
    form = TaskForm(dtype='technical_design')

  context = {
      "obj_list": new_data,
      "form": form,
      "title": 'Technical Design',
  }
  return render(request, "design_health/design_task_list.html", context)


@login_required()
def developed_design_view(request):
  categories = DesignCategory.objects.all()
  tasks = Task.objects.filter(design_type='developed_design')
  new_data = {}
  for category in categories:
    new_data[category.name] = []
    for task in tasks:
      if task.design_category == category:
        new_data[category.name].append(task)

  if request.method == 'POST':
    form = TaskForm('developed_design', request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.design_type = 'developed_design'
      form.save()
      messages.success(request, 'Task successfully added.')
      return redirect(request.path)
  else:
    form = TaskForm(dtype='developed_design')

  context = {
      "obj_list": new_data,
      "form": form,
      "title": 'Developed Design',
  }
  return render(request, "design_health/design_task_list.html", context)


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, AjaxableResponseMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = '__all__'
    template_name = 'design_health/new_task.html'
    success_message = 'New task added'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        return self.request.user.is_superuser


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'design_health/edit_task.html'
    success_message = 'Task has been successfully updated.'

    def get_success_url(self):
      obj = self.object
      de_type = (obj.design_type).replace("_", "-")
      return reverse_lazy(de_type)

    def test_func(self):
        return self.request.user.is_superuser


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'design_health/delete_form.html'

    def get_success_url(self):
      obj = self.object
      de_type = (obj.design_type).replace("_", "-")
      return reverse_lazy(de_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Task Delete"
        return context

    def test_func(self):
        return self.request.user.is_superuser


@login_required()
def manage_projects(request):
  project_form = ProjectForm()
  company_form = CompanyForm()
  project_search = SearchProject(initial={
    "project": request.GET.get('project'),
    "company": request.GET.get('company'),
  })
  search_result = Project.objects.none() 
  edit_form = ''
  project_role_form = ''
  concept_tasks = Task.objects.filter(design_type='concept_design')
  developed_tasks = Task.objects.filter(design_type='developed_design')
  technical_tasks = Task.objects.filter(design_type='technical_design')
  project_task_form_concept = ''
  project_task_form_developed = ''
  project_task_form_technical = ''
  pp = ''

  if request.GET.get('pk'):
    pp = Project.objects.get(pk=request.GET.get('pk'))
    edit_form = EditForm(instance=pp)
    initials = []
    roles = Role.objects.all()
    projectroles = ProjectRole.objects.filter(project=pp)
    for role in roles:
      if role not in [prs.role for prs in projectroles]:
        initials.append({
          "role":role,
        })


    project_role_form = ProjectRoleForm(
      instance=pp,
      initial=initials,
      prefix='project_role_form',
    )
    project_role_form.extra=len(roles)
    project_role_form.max_num=len(roles)

    #concept design task
    projecttasks = ProjectTask.objects.filter(project=pp)

    ctinitials= [{"task":task} for task in concept_tasks if task not in [ptsk.task for ptsk in projecttasks]]
    project_task_form_concept = ProjectTaskForm(
      instance = pp,
      initial=ctinitials,
      prefix='project_task_form_concept',
    )
    project_task_form_concept.extra=len(concept_tasks)
    project_task_form_concept.max_num=len(concept_tasks)

    #developed_Design
    dtinitials= [{"task":task} for task in developed_tasks if task not in [ptsk.task for ptsk in projecttasks]]
    project_task_form_developed = ProjectTaskForm(
      instance = pp,
      initial=dtinitials,
      prefix='project_task_form_developed',
    )
    project_task_form_developed.extra=len(developed_tasks)
    project_task_form_developed.max_num=len(developed_tasks)

    #technical_design
    ttinitials= [{"task":task} for task in technical_tasks if task not in [ptsk.task for ptsk in projecttasks]]
    project_task_form_technical = ProjectTaskForm(
      instance = pp,
      initial=ttinitials,
      prefix='project_task_form_technical',
    )
    project_task_form_technical.extra=len(technical_tasks)
    project_task_form_technical.max_num=len(technical_tasks)
    
    
  if request.GET.get('project') and request.GET.get('searchbyproject'):
    search_result = Project.objects.filter(project_name__icontains=request.GET.get('project'))

  if request.GET.get('company') and request.GET.get('searchbyclient'):
    search_result = Project.objects.filter(client_id=request.GET.get('company'))

  if request.method == 'POST':
    project_form = ProjectForm(request.POST)
    if project_form.is_valid():
        project_form.save() 
    
    #project role
    if 'project_role_form' in request.POST:
      project_role_form = ProjectRoleForm(
        request.POST, 
        instance=pp,
        initial=initials,
        prefix='project_role_form',
      )
      if project_role_form.is_valid():
        project_role_form.save()
        messages.success(request, 'Project roles successfully updated')
        return redirect(reverse('manage-projects') + '?pk='+request.GET.get('pk'))

    #concept task
    if 'project_task_form_concept' in request.POST:
      project_task_form_concept = ProjectTaskForm(
        request.POST,
        instance=pp,
        initial=ctinitials,
        prefix='project_task_form_concept',
      )
      if project_task_form_concept.is_valid():
        project_task_form_concept.save()
        messages.success(request, 'Tasks successfully updated.')
        return redirect(reverse('manage-projects') + '?pk='+request.GET.get('pk'))

    #developed task
    if 'project_task_form_developed' in request.POST:
      project_task_form_developed = ProjectTaskForm(
        request.POST,
        instance=pp,
        initial=dtinitials,
        prefix='project_task_form_developed',
      )
      if project_task_form_developed.is_valid():
        project_task_form_developed.save()
        messages.success(request, 'Tasks successfully updated.')
        return redirect(reverse('manage-projects') + '?pk='+request.GET.get('pk'))
    
    #concept task
    if 'project_task_form_technical' in request.POST:
      project_task_form_technical = ProjectTaskForm(
        request.POST,
        instance=pp,
        initial=ttinitials,
        prefix='project_task_form_technical',
      )
      if project_task_form_technical.is_valid():
        project_task_form_technical.save()
        messages.success(request, 'Tasks successfully updated.')
        return redirect(reverse('manage-projects') + '?pk='+request.GET.get('pk'))

    

  context = {
    "project_search": project_search,
    "search_result": search_result,
    "edit_form": edit_form,
    "project_role_form": project_role_form,
    "project_task_form_concept": project_task_form_concept,
    "project_task_form_technical": project_task_form_technical,
    "project_task_form_developed": project_task_form_developed,
    "project_form": project_form,
    "company_form": company_form,
  }
  return render(request, 'design_health/manage_projects.html', context)


  
class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, AjaxableResponseMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = '__all__'
    success_message = 'New project added'
    success_url = reverse_lazy('manage-projects')

    def test_func(self):
        return self.request.user.is_superuser
