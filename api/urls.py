from os import name
from django.urls import path
from django.urls.conf import include

from rest_framework.routers import DefaultRouter



from .views import *


router = DefaultRouter()

router.register('universite', UniversiteApiView, basename='universite')
router.register('faculte', FaculteApiView, basename='faculte')
router.register('departement', DepartementApiView, basename='departement')
router.register('promotion', PromotionApiView, basename='promotion')
router.register('cours', CoursApiView, basename='cours')
router.register('enseignant', EnseignantApiView, basename='enseignant')
router.register('etudiant', EtudiantApiView, basename='etudiant')
router.register('cotes', CotesApiView, basename='cotes')



urlpatterns = [

    path('', include(router.urls)),
    # path('cote/', CoteApiView.as_view(), name="cote"),
    
]
