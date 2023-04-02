from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('classify/', views.classify, name='classify'),
    path('building/<bin>', views.building, name='building'),
    path('compare/area/<id>', views.areacompare, name='areacompare'),
    path('compare/purpose/<id>', views.purposecompare, name='purposecompare'),
    path('compare/zipcode/<id>', views.zipcodecompare, name='zipcodecompare')
]