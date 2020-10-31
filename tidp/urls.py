from django.urls import path

from . import views

app_name = 'tidp'

urlpatterns = [
    path('roles/', views.role_list_view, name='roles'),
    path('roles/<int:pk>/update/', views.RoleUpdateView.as_view(), name="role-update"),
    path('roles/<int:pk>/delete/', views.RoleDeleteView.as_view(), name="role-delete"),

    path('company/list/', views.CompanyListView.as_view(),
       name='company-list'),
    path('company/create/', views.CompanyCreateView.as_view(),
        name='create-company'),
    path('company/<int:pk>/update/', views.CompanyUpdateView.as_view(), name="company-update"),
    path('company/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name="company-delete"),

    path('projects/', views.ManageProjects.as_view(), name='projects'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/manage/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/lmanage/', views.ProjectDetailLeaderView.as_view(), name='project-detail-leader'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/submit-to-lead/', views.ProjectSubmitToLeadView.as_view(), name='project-submit-to-lead'),
    path('projects/role-status-update/<int:projectrole_id>/', views.RoleStatusUpdateView.as_view(), name='role-status-update'),

    path('project-discipline/', views.DisciplineListView.as_view(), name='project-discipline'),
    path('project-discipline/create/', views.DisciplineCreateView.as_view(), name='discipline-create'),
    path('discipline/<int:pk>/update/', views.DisciplineUpdateView.as_view(), name='update-discipline'),
    path('discipline/<int:pk>/delete/', views.DisciplineDeleteView.as_view(), name='delete-discipline'),

    path('discipline-categories/', views.DisciplineCategoryListView.as_view(), name='project-discipline-categories'),
    path('discipline-categories/create/', views.DisciplineCategoryCreateView.as_view(), name='discipline-category-create'),
    path('discipline-categories/<int:pk>/update/', views.DisciplineCategoryUpdateView.as_view(), name='update-discipline-category'),
    path('discipline-categories/<int:pk>/delete/', views.DisciplineCategoryDeleteView.as_view(), name='delete-discipline-category'),

    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name="task-update"),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name="task-delete"),

    path('tasktype/', views.TaskTypeView.as_view(), name='tasktypes'),
    path('tasktype/create/', views.TaskTypeCreateView.as_view(), name='tasktype-create'),
    path('tasktype/<int:pk>/update/', views.TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path('tasktype/<int:pk>/delete/', views.TaskTypeDeleteView.as_view(), name="tasktype-delete"),

    path('taskleader/<int:project_id>/create/', views.TaskLeaderCreateView.as_view(), name="taskleader-create"),
    path('taskleader/<int:pk>/update/', views.TaskLeaderUpdateView.as_view(), name="update-taskleader"),
    path('taskleader/<int:pk>/delete/', views.TaskLeaderDeleteView.as_view(), name="delete-taskleader"),

    path('taskmember/<int:project_id>/create/', views.TaskMemberCreateView.as_view(), name="taskmember-create"),
    path('taskmember/<int:pk>/update/', views.TaskMemberUpdateView.as_view(), name="taskmember-update"),
    path('taskmember/<int:pk>/delete/', views.TaskMemberDeleteView.as_view(), name="taskmember-delete"),

    path('export-tasks/<int:project_id>/<int:role>/', views.export_task_to_csv, name='export-tasks'),

    path('projecttask/<int:project_id>/<int:discipline>/<int:discipline_category>/<int:role>/<int:company>/create/', views.ProjectTaskCreateView.as_view(), name="projecttask-create"),

    path('projecttask-duplicate/', views.ProjectTaskDuplicateView.as_view(), name="projecttask-createmultiple"),

    path('projecttask/<int:pk>/update/', views.ProjectTaskUpdateView.as_view(), name="projecttask-update"),
    path('projecttask/<int:pk>/delete/', views.ProjectTaskDeleteView.as_view(), name="projecttask-delete"),
    path('tasks/<int:pk>/detail/', views.ProjectTaskDetailView.as_view(), name="task-detail"),

    path('roles/import/', views.import_roles, name='import-roles'),

    path('tasktype/import/', views.import_tasktypes, name='import-tasktypes'),

    path('projecttask/import/', views.import_tasks, name='import-projecttask'),

    path('projecttask/import/<int:project_id>/<int:role>/', views.import_project_task, name='import-projecttask-project'),

    path('get-company/', views.get_company, name='get-company'),
    path('get-disciplinecategory/', views.get_disciplinecategory, name='get-disciplinecategory'),

    path('mark-complete/<int:project_id>/<int:role_id>/<int:company_id>/', views.CompleteTaskPage.as_view(), name='mark-complete'),


    path('generate-tidp/<int:project_id>/<int:projectrole_id>/', views.GenerateTidpMidp.as_view(), name='generate-tidp'),
    path('generate-midp/<int:project_id>/', views.GenerateTidpMidp.as_view(), name='generate-midp'),

    path('view-tidp/<int:project_id>/<int:projectrole_id>/', views.ViewTidpMidp.as_view(), name='view-tidp'),
    path('view-midp/<int:project_id>/', views.ViewTidpMidp.as_view(), name='view-midp'),


    path('download-template/<content_type>/', views.download_exl_template, name='download-template'),

    path('project-scales', views.ProjectScaleView.as_view(), name='project-scales'),

    path('project-scales/<int:pk>/update/', views.ProjectScaleUpdateView.as_view(), name='project-scales-update'),

    path('project-scales/<int:pk>/delete/', views.ProjectScaleDeleteView.as_view(), name='project-scales-delete'),
]

