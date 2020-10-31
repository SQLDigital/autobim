from django.urls import path, re_path

from . import views

urlpatterns = [
  path('roles/', views.role_list_view, name='design-roles'),
  path('roles/<int:pk>/update/', views.RoleUpdateView.as_view(), name='update-role'),
  path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='delete-role'),

  path('company/list/', views.CompanyListView.as_view(),
       name='company-list'),
  path('company/create/', views.CompanyCreateView.as_view(),
        name='create-company'),
  path('company/<int:pk>/update/',
        views.CompanyUpdateView.as_view(), name='update-company'),
  path('company/<int:pk>/delete/',
        views.CompanyDeleteView.as_view(), name='delete-company'),

  path('design-categories/', views.design_categories_view,
       name='design-categories'),
  path('design-categories/<int:pk>/update/', views.DesignCategoryUpdateView.as_view(), name='design-category-update'),
  path('design-categories/<int:pk>/delete/', views.DesignCategoryDeleteView.as_view(), name='design-category-delete'),

  path('concept-design', views.concept_design_view, name='concept-design'),
  path('developed-design', views.developed_design_view, name='developed-design'),
  path('technical-design', views.technical_design_view, name='technical-design'),
  path('tasks/create/', views.TaskCreateView.as_view(), name='design-task-create'),
  path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='design-task-update'),
  path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='design-task-delete'),

  path('manage-projects/', views.manage_projects, name='manage-projects'),
  path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),

]
