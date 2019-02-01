from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('statistics/', views.statistics),
    path('rank/', views.ranking),
    path('update_all_members_88339988/', views.update_database_all_member)
]