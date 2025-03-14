from django.urls import path
from core.views.basic_view import ping
from django.urls import path
from core.views.role_view import RoleListView, RoleDetailView
from core.views.course_view import CourseListView, CourseDetailView, CourseSearchView
from core.views.employee_view import EmployeeListView, EmployeeDetailView

urlpatterns = [
    path('ping/', ping, name='ping'),  # Exposes /ping
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:role_id>/', RoleDetailView.as_view(), name='role-detail'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('courses/search/', CourseSearchView.as_view(), name='course-search'),
]
