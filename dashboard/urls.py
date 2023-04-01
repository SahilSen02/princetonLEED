from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('classify/', views.classify, name='classify'),
    path('building/<bin>', views.building, name='building')
]