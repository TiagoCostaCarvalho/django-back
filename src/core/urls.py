from django.urls import path
from core.views.basic_view import ping
from core.views.role_view import RoleListView
 
urlpatterns = [
    path('ping/', ping, name='ping'),  # Exposes /ping
    path('roles/', RoleListView.as_view(), name='role-list'),
]
