from django.db import models



class Universite(models.Model):
    nom_univ = models.CharField(max_length=50)
    single = models.CharField(max_length=10)

    # admin = models.OneToOneField("app.Model", on_delete=models.CASCADE)


    def __str__(self):
        return self.single



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

    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom_prom



class Enseignant(models.Model):
    nom_enseigant = models.CharField(max_length=20)
    post_nom_enseignant = models.CharField(max_length=20)
    num_tel = models.CharField(max_length=15)

    # user = models.OneToOneField("app.Model", verbose_name=_(""), on_delete=models.CASCADE)

    def __str__(self):
        return f"${self.nom} ${self.post_nom}"




class Cours(models.Model):
    code = models.CharField(max_length=20)
    nom_course = models.CharField(max_length=50)

    promotion = models.ManyToManyField(Promotion)
    enseignant = models.OneToOneField(Enseignant, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom_course



class Etudiant(models.Model):
    matricule = models.CharField(max_length=20)
    nom_etudiant = models.CharField(max_length=20)
    post_nom_etudiant = models.CharField(max_length=20)
    prenom_etudiant = models.CharField(max_length=20)

    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    def __str__(self):
        return f"${self.matricule} ${self.prenom_etudiant}"
