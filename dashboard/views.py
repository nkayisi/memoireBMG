import csv
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.generic import TemplateView
from django.conf import settings


from django.contrib.auth.hashers import make_password


from django.contrib import messages

from api.models import *

from .forms import CotesForm


from api.utils import create_csv, write_csv

import json
import csv
import requests


@login_required
def nouvelle_cote(request, cours_id):
    form = CotesForm()
    if request.method == 'POST':
        form = CotesForm(request.POST)
        if form.is_valid():
            # recuperer les donnees du formulaire
            label = request.POST['label']
            ponderation = request.POST['ponderation']
            date = request.POST['date']

            # recuperer les etudiants
            etudiants = Etudiant.objects.all()

            # trouver le cours pour lequel on cree la fiche des cotes
            cours = Cours.objects.get(id=cours_id)

            # recuperer le dernier code de cours enfin de l'incrementer pour creer le nouveau
            cote = None
            try:
                cote = Cotes.objects.latest('id')
                code = int(cote.code) + 1
                print('Cote label', cote.code)
            except:
                code = 1

            # creer les objets cote a partir des la liste des etudiants
            for et in etudiants:
                print(label,cote,ponderation,date,cours,code,)
                Cotes.objects.create(
                    label = label,
                    cote = None,
                    ponderation = ponderation,
                    date = date,
                    cours = cours,
                    code = code,
                    etudiant = et
                )

        return redirect('cotes')
    return render(request, 'dashboard/pages/nouvelle_cote.html', {'form': form, 'cours_id':cours_id})


def loginView(request):

    if request.method == 'POST':

        nom_utilisateur = request.POST.get('nom_utilisateur')
        mot_de_passe = request.POST.get('motDePasse')

        user = authenticate(username=nom_utilisateur, password=mot_de_passe)

        print(user)

        if user is not None:

            group = user.groups.all()[0]

            if user.is_active and group.name == 'admin':
                login(request, user)
                return redirect('accueil')
            elif group.name != 'admin':
                login(request, user)
                return redirect('cotes')

    return render(request, "dashboard/pages/login.html")




@login_required
def accueil(request):

    univ = request.user.universite
    departements = []
    cours = []

    facultes = univ.faculte_set.all()
    promotions = univ.promotion_set.all()

    for faculte in facultes:
        departs = faculte.departement_set.all()
        for depart in departs:
            departements.append(depart)


    for departement in departements:
        crs = departement.cours_set.all()
        for cr in crs:
            cours.append(cr)

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
        'cours': cours,
        'total_depart': len(departements),
        'total_cours': len(cours)
    }

    return render(request, 'dashboard/pages/index.html', context)


@login_required
def cotes(request):
    try:
        enseignant = Enseignant.objects.get(user=request.user)
        cours = Cours.objects.filter(enseignant=enseignant)
        pass
    except:
        messages.success(request, 'Connectez-vous avec un compte enseignant')
        return redirect('login')

    context={
        'cours':cours
    }
    return render(request, 'dashboard/pages/cotes.html', context)


def SomeFunction(request):
    cotes = json.loads(request.GET['cotes'])

    course_name = request.GET.get('course_name')
    print(course_name)
    
    file = open(f'{course_name}', 'w')

    writer = csv.writer(file)

    writer.writerow(['Matricules', 'TP', 'TD', 'Intérogation', 'Examen', 'Total'])
    
    for cote in cotes:
        writer.writerow([cote.get('Matricule'),cote.get('TP'),cote.get('TD'),cote.get('Interro'),cote.get('Examen')])
        
    return HttpResponse("OK")



def download_csv(request, course_id):
    cours = Cours.objects.get(id=course_id)
    req = requests.get('http://127.0.0.1:8000/'+cours.cote.url)
    url_content = req.content
    csv_file = open(f'cotes/{cours.nom_cours}.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

    return redirect('cours')


@login_required
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
            password = make_password(motDePasse)
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


@login_required
def etudiant(request):


    univ = request.user.universite
    departements = []
    cours = []
    etudiants = []

    facultes = univ.faculte_set.all()
    promotions = univ.promotion_set.all()

    for faculte in facultes:
        departs = faculte.departement_set.all()
        for depart in departs:
            departements.append(depart)


    for departement in departements:
        crs = departement.cours_set.all()
        ets = departement.etudiant_set.all()
        for cr in crs:
            cours.append(cr)

        for et in ets:
            etudiants.append(et)



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

@login_required
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
        admin = User.objects.create_user(
            username=nom_utilisateur, 
            email=email,
            password = make_password(motDePasse)
            )
        
        group = Group.objects.get(name='admin')
        admin.groups.add(group)
        admin.is_staff = True
        admin.save()

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


@login_required
def profile(request):
    return render(request, 'dashboard/pages/profile.html')


@login_required
def cours(request):

    univ = request.user.universite
    departements = []
    cours = []
    etudiants = []

    facultes = univ.faculte_set.all()
    promotions = univ.promotion_set.all()

    for faculte in facultes:
        departs = faculte.departement_set.all()
        for depart in departs:
            departements.append(depart)


    for departement in departements:
        crs = departement.cours_set.all()
        ets = departement.etudiant_set.all()
        for cr in crs:
            cours.append(cr)

        for et in ets:
            etudiants.append(et)

 
    enseignants = Enseignant.objects.all()


    if request.method == 'POST':

        # Course fields
        code =  request.POST.get('code')
        titre_cours =  request.POST.get('titre_cours')
        id_depart =  request.POST.get('departement').split('-')[0]
        depart = Departement.objects.get(id=id_depart)
        id_prom =  request.POST.get('promotion').split('-')[0]
        prom = Promotion.objects.get(id=id_prom)
        id_enseignant =  request.POST.get('enseignant').split('-')[0]

        file = create_csv(titre_cours, depart, prom)

        Cours.objects.create(
            code = code,
            nom_cours = titre_cours,
            departement = depart,
            promotion = prom,
            enseignant = Enseignant.objects.get(id=id_enseignant),
            cote = file
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



@login_required
def logOut(request):
    logout(request)
    return redirect('login')