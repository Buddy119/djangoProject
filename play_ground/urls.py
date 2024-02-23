from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('ask_document', views.ask_document),
    path('user_story', views.user_story),
    path('test_scenario', views.test_scenario),
    path('test_script', views.test_script),
    path('gpt', views.test_gpt),
    path('agent', views.test_agent)
]