from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    path('show-servers/', views.show_servers, name="show_servers"),
    path('show-procstat/', views.show_procstat, name="show_procstat"),


]



