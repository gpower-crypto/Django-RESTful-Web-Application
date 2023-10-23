from django.urls import include, path
from rest_framework import routers
from . import views, api

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.displayHomePage, name='displayHomePage'),  # display the home page with a list of API endpoints
    path('api/protein/', api.add_record),  # endpoint for protein detail API
    path('api/protein/<str:id>', api.protein_detail, name='protein_api'),  # endpoint for protein detail API
    path('api/pfam/<str:id>', api.pfam_detail, name='domain_api'),  # endpoint for pfam domain detail API
    path('api/proteins/<int:id>', api.taxonomy_detail),  # endpoint for retrieving taxonomy details with associated proteins
    path('api/pfams/<int:id>', api.taxonomy_detail),  # endpoint for retrieving taxonomy details with associated pfam domains
    path('api/coverage/<str:id>', api.coverage, name='coverage_api')  # endpoint for calculating protein coverage
]
