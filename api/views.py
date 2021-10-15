from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import *

from .serializers import *





class UniversiteApiView(ModelViewSet):
    serializer_class = UniversiteSerializer

    def get_queryset(self):
        return Universite.objects.all()


    def create(self, request, *args, **kwargs):
        universiteData = request.data
        newUniversite = Universite.objects.create(
            nom_univ = universiteData['nom_univ'],
            sigle = universiteData['single']
        )
        newUniversite.save()
        serializer = UniversiteSerializer(newUniversite)
        return Response(serializer.data)




class FaculteApiView(ModelViewSet):
    serializer_class = FaculteSerializer

    def get_queryset(self):
        return Faculte.objects.all()


    def create(self, request, *args, **kwargs):
        faculteData = request.data
        newFaculte = Faculte.objects.create(
            nom_fac = faculteData['nom_fac'],
            universite = Universite.objects.get(id=faculteData['universite'])
        )
        newFaculte.save()
        serializer = FaculteSerializer(newFaculte)
        return Response(serializer.data)
    
    


class DepartementApiView(ModelViewSet):
    serializer_class = DepartementSerializer

    def get_queryset(self):
        return Departement.objects.all()


    def create(self, request, *args, **kwargs):
        departemtData = request.data
        newDepartement = Departement.objects.create(
            nom_depart = departemtData['nom_depart'],
            faculte = Faculte.objects.get(id=departemtData['faculte'])
        )
        newDepartement.save()
        serializer = DepartementSerializer(newDepartement)
        return Response(serializer.data)




class PromotionApiView(ModelViewSet):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        return Promotion.objects.all()

    
    def create(self, request, *args, **kwargs):
        promotionData = request.data
        newPromotion = Promotion.objects.create(
            nom_prom = promotionData['nom_prom'],
            departement = Departement.objects.get(id=promotionData['departement'])
        )
        newPromotion.save()
        serializer = PromotionSerializer(newPromotion)
        return Response(serializer.data)




class CoursApiView(ModelViewSet):
    serializer_class = CoursSerializer

    def get_queryset(self):
        return Cours.objects.all()


    def create(self, request, *args, **kwargs):
        coursData = request.data
        newCours = Cours.objects.create(
            code = coursData['code'],
            nom_cours = coursData['nom_cours'],
            promotion = Promotion.objects.get(id=coursData['promotion']),
            enseignant = Enseignant.objects.get(id=coursData['enseignant']),
        )
        newCours.save()
        serializer = CoursSerializer(newCours)
        return Response(serializer.data)



class EnseignantApiView(ModelViewSet):
    serializer_class = EnseignantSerializer

    def get_queryset(self):
        return Enseignant.objects.all()


    def create(self, request, *args, **kwargs):
        enseignantData = request.data
        newEnseignant = Enseignant.objects.create(
            nom_enseigant = enseignantData['nom_enseigant '],
            post_nom_enseignant = enseignantData['post_nom_enseignant'],
            num_tel = enseignantData['num_tel']
        )
        newEnseignant.save()
        serializer = EnseignantSerializer(newEnseignant)
        return Response(serializer.data)




class EtudiantApiView(ModelViewSet):
    serializer_class = EtudiantSerializer

    def get_queryset(self):
        return Etudiant.objects.all()


    def create(self, request, *args, **kwargs):
        etudiantData = request.data
        newEtudiant = Etudiant.objects.create(
            matricule = etudiantData['matricule '],
            nom_etudiant = etudiantData['nom_etudiant '],
            post_nom_etudiant = etudiantData['post_nom_etudiant'],
            prenom_etudiant = etudiantData['prenom_etudiant'],

            promotion = Promotion.objects.get(id=etudiantData['promotion']),
        )
        newEtudiant.save()
        serializer = EtudiantSerializer(newEtudiant)
        return Response(serializer.data)