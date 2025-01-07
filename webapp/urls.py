# urls.py for webapp


    
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name='logout'),
    path('create-record', views.create_record, name='create-record'),
    path('update-record/<str:pk>', views.update_record, name='update-record'),
    path('view-record/<str:pk>', views.singular_record, name='view-record'),
    path('delete-record/<str:pk>', views.delete_record, name='delete-record'),
]