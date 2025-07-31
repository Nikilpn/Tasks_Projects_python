
from django.urls import path
from displayapp import views
urlpatterns=[
    path('home/', views.index_page, name='index'),
    
]