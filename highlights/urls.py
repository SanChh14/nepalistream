from django.urls import path
from . import views

urlpatterns = [
    path('', views.highlights, name = 'highlights'),

]
