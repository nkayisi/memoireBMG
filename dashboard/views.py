from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib import messages

from api.models import *


def accueil(request):

    facultes = Faculte.objects.all()
    departements = Departement.objects.all()
    promotions = Promotion.objects.all()
    cours = Cours.objects.all()

    univ = Universite.objects.get(admin=request.user)

    if request.method == 'POST':
        nom_fac = request.POST.get('nom_fac')

        nom_depart = request.POST.get('nom_depart')

        nom_prom = request.POST.get('nom_prom')

        if nom_fac:

            Faculte.objects.create(
                nom_fac = nom_fac,
                universite = univ
            )

            # Push a message on the template
            messages.success(request, 'Faculté ajouter avec succès dans '+ univ.sigle)

        elif nom_depart:

            id_fac = request.POST.get('faculte').split('-')[0]

            Departement.objects.create(
                nom_depart = nom_depart,
                faculte = Faculte.objects.get(id=id_fac)
            )

            # Push a message on the template
            messages.success(request, 'Département ajouter avec succès dans '+ univ.sigle)

        elif nom_prom:

            Promotion.objects.create(
                nom_prom = nom_prom,
                universite = univ
            )

            # Push a message on the template
            messages.success(request, 'Promotion ajouter avec succès dans '+ univ.sigle)

    context = {
        'facultes': facultes,
        'departements': departements,
        'promotions': promotions,
        'cours': cours
    }

    return render(request, 'dashboard/pages/index.html', context)



def cotes(request):
    return render(request, 'dashboard/pages/cotes.html')



def enseignant(request):

    if request.method == 'POST':

        # Teacher fields
        nom = request.POST.get('nom')
        post_nom = request.POST.get('post_nom')
        nom_utilisateur = request.POST.get('nom_utilisateur')
        email = request.POST.get('email')
        motDePasse = request.POST.get('motDePasse')
        tel = request.POST.get('phoneNumber')

        # Create teacher's user
        user = User.objects.create(
            username = nom_utilisateur,
            email = email,
            password = motDePasse
        )

        # Set a group to the teacher's user
        group = Group.objects.get(name="enseignant")
        user.groups.add(group)

        # Create teacher
        Enseignant.objects.create(
            nom_enseignant = nom,
            post_nom_enseignant = post_nom,
            num_tel = tel,
            user = user
        )

        # Push a message on the template
        messages.success(request, 'Enseignant ajouter avec succès par '+ request.user.username)


    return render(request, 'dashboard/pages/enseignant.html')



def etudiant(request):

    departements = Departement.objects.all()
    promotions = Promotion.objects.all()
    etudiants = Etudiant.objects.all()

    if request.method == 'POST':

        # Student fields
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        post_nom = request.POST.get('post_nom')
        prenom = request.POST.get('prenom')
        id_depart = request.POST.get('departement').split('-')[0]
        id_prom = request.POST.get('promotion').split('-')[0]

        Etudiant.objects.create(
            matricule = matricule,
            nom_etudiant = nom,
            post_nom_etudiant = post_nom,
            prenom_etudiant = prenom,
            departement = Departement.objects.get(id=id_depart),
            promotion = Promotion.objects.get(id=id_prom)
        )

        # Push a message on the template
        messages.success(request, 'Etudiant ajouter avec succès par '+ request.user.username)

    context = {
        'departements': departements,
        'promotions': promotions,
        'etudiants': etudiants
    }

    return render(request, 'dashboard/pages/etudiant.html', context)


def universite(request):

    if request.method == 'POST':

        # University fields
        nom_univ = request.POST.get('nom_univ')
        sigle = request.POST.get('sigle')
        bp = request.POST.get('bp')

        # Admin fields
        nom_utilisateur = request.POST.get('nom_utilisateur')
        email = request.POST.get('email')
        motDePasse = request.POST.get('motDePasse')
        
        # Create admin account
        admin = User.objects.create(
            username=nom_utilisateur, 
            email=email,
            password= motDePasse
            )
        group = Group.objects.get(name='admin')
        admin.groups.add(group)

        print(admin)

        # Create university
        Universite.objects.create(
            nom_univ=nom_univ,
            sigle=sigle, 
            bp=bp,
            admin=admin
        )


        # Push a message on the template
        messages.success(request, 'Salut ' + request.user.username 
                + ', le compte que vous venez de crée a réussit avec succès...')


        
    return render(request, 'dashboard/pages/universite.html')



def profile(request):
    return render(request, 'dashboard/pages/profile.html')



def cours(request):

    departements = Departement.objects.all()
    promotions = Promotion.objects.all()
    enseignants = Enseignant.objects.all()
    cours = Cours.objects.all()

    if request.method == 'POST':

        # Course fields
        code =  request.POST.get('code')
        titre_cours =  request.POST.get('titre_cours')
        id_depart =  request.POST.get('departement').split('-')[0]
        id_prom =  request.POST.get('promotion').split('-')[0]
        id_enseignant =  request.POST.get('enseignant').split('-')[0]

        Cours.objects.create(
            code = code,
            nom_cours = titre_cours,
            departement = Departement.objects.get(id=id_depart),
            promotion = Promotion.objects.get(id=id_prom),
            enseignant = Enseignant.objects.get(id=id_enseignant)
        )

        # Push a message on the template
        messages.success(request, 'Cours ajouter avec succès par '+ request.user.username)

    context = {
        'departements': departements,
        'promotions': promotions,
        'enseignants': enseignants,
        'cours': cours
    }
    return render(request, 'dashboard/pages/cours.html', context)