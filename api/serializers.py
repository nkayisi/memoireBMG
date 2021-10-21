from rest_framework import serializers


from .models import *


class UniversiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universite
        fields = '__all__'



class FaculteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculte
        fields = '__all__'
        depth = 1



class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'
        depth = 2



class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
        depth = 3



class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = '__all__'
        depth = 4



class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'
        depth = 1


class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'
        depth = 4


class CotesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cotes
        fields= '__all__'
