from django.db import models

from django.contrib.auth.models import User
from django.db.models.enums import Choices



class Universite(models.Model):
    nom_univ = models.CharField(max_length=50)
    sigle = models.CharField(max_length=10)
    bp = models.CharField(max_length=20, blank=True, null=True)

    admin = models.OneToOneField(User, on_delete=models.CASCADE , blank=True, null=True)


    def __str__(self):
        return self.sigle



class Faculte(models.Model):
    nom_fac = models.CharField(max_length=50)

    universite = models.ForeignKey(Universite, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom_fac



class Departement(models.Model):
    nom_depart = models.CharField(max_length=50)

    faculte = models.ForeignKey(Faculte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_depart



class Promotion(models.Model):
    nom_prom = models.CharField(max_length=50)

    universite = models.ForeignKey(Universite, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_prom



class Enseignant(models.Model):
    nom_enseignant = models.CharField(max_length=20)
    post_nom_enseignant = models.CharField(max_length=20)
    num_tel = models.CharField(max_length=15)

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.nom_enseignant} {self.post_nom_enseignant}"




class Cours(models.Model):
    code = models.CharField(max_length=20)
    nom_cours = models.CharField(max_length=50)

    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)

    cote = models.FileField(upload_to='cotes/', max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nom_cours



class Etudiant(models.Model):
    matricule = models.CharField(max_length=20)
    nom_etudiant = models.CharField(max_length=20)
    post_nom_etudiant = models.CharField(max_length=20)
    prenom_etudiant = models.CharField(max_length=20)


    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.matricule} - {self.nom_etudiant} - {self.prenom_etudiant}"


class Cotes(models.Model):
    LABELS =(
        ("TP", "Travail Pratique"),
        ("TD", "Travail Dirigé"),
        ("INT", "Interrogation"),
        ("EX", "Examen"),
    )
    label=models.CharField(max_length=50,choices=LABELS, verbose_name='Type de travail')
    cote=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ponderation=models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Pondération')
    etudiant= models.ForeignKey(Etudiant, on_delete=models.CASCADE )
    date=models.DateField(auto_now=False, verbose_name='A remettre le')
    cours=models.ForeignKey(Cours, on_delete=models.CASCADE)
    code=models.IntegerField(default=0)

    def __str__(self):
        return self.label

