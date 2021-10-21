import csv
from django.db.models.aggregates import Sum
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
from requests.models import Response
import urllib3

from api.models import *

from .forms import CotesForm


from api.utils import create_csv, write_csv

import json
import csv
import requests
from django.db.models import Count

# Import mimetypes module
import mimetypes
# Import HttpResponse module
from django.http.response import HttpResponse



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
            ponderation_blobal = request.POST['ponderation_blobal']

            # trouver le cours pour lequel on cree la fiche des cotes
            cours = Cours.objects.get(id=cours_id)

            # recuperer les etudiants
            etudiants = Etudiant.objects.all().filter(
                departement=cours.departement, promotion=cours.promotion)

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
                print(label,cote,ponderation,date,cours,code,ponderation_blobal)
                Cotes.objects.create(
                    label = label,
                    cote = None,
                    ponderation = ponderation,
                    date = date,
                    ponderation_blobal = ponderation_blobal,
                    cours = cours,
                    code = code,
                    etudiant = et
                )

        return redirect('cotes',cours_id)
    return render(request, 'dashboard/pages/nouvelle_cote.html', {'form': form, 'cours_id':cours_id})


@login_required
def coter(request):
    
    cote = request.GET.get('cote', None)
    travail_id = request.GET.get('travail_id', None)
    
    travail = get_object_or_404(Cotes, id=travail_id)
    travail.cote = cote
    travail.save()
    
    return HttpResponse('OK')


@login_required
def envoieCotes(request, cours_id):

    cours = get_object_or_404(Cours, id=cours_id)
    cotes = Cotes.objects.all().filter(cours=cours_id)
    etudiants = Etudiant.objects.all().filter(departement=cours.departement, 
                promotion=cours.promotion)


    file = open(f'cotes/{cours.nom_cours}.csv', 'w')

    writer = csv.writer(file)

    writer.writerow(['Titre du cours : '+cours.nom_cours])
    writer.writerow(['Nom de l\'enseigant : '
                    +cours.enseignant.nom_enseignant +' '
                    + cours.enseignant.post_nom_enseignant])
    writer.writerow(['Matricules', 'TP', 'TD', 'Intérogation', 'Examen', 'Total'])
    
    

    tps = cotes.filter(label='TP')
    tds = cotes.filter(label='TD')
    et_ints = cotes.filter(label='INT')
    et_exs = cotes.filter(label='EX')

    for etudiant in etudiants:

        et_tps = tps.filter(etudiant=etudiant)
        et_tds = tds.filter(etudiant=etudiant)
        et_ints = et_ints.filter(etudiant=etudiant)
        et_exs = et_exs.filter(etudiant=etudiant)

        row = [etudiant.matricule]
        totalMoyenne = 0;

        if et_tps:
            total = 0;
            moyenne = 0;
            sommePonderation = 0;
            
            for et_tp in et_tps:
                total += et_tp.cote
                sommePonderation+=et_tp.ponderation
            moyenne = (total/sommePonderation)*et_tps[0].ponderation_blobal

            row.append(moyenne)
            totalMoyenne += moyenne

        if et_tds:
            total = 0;
            moyenne = 0;
            sommePonderation = 0;
            for et_td in et_tds:
                total += et_td.cote
                sommePonderation+=et_td.ponderation
            moyenne = (total/sommePonderation)*et_tds[0].ponderation_blobal

            row.append(moyenne)
            totalMoyenne += moyenne

        if et_ints:
            total = 0;
            moyenne = 0;
            sommePonderation = 0;
            for et_int in et_ints:
                total += et_int.cote
                sommePonderation+=et_int.ponderation
            moyenne = (total/sommePonderation)*et_ints[0].ponderation_blobal

            row.append(moyenne)
            totalMoyenne += moyenne


        if et_exs:
            total = 0;
            moyenne = 0;
            sommePonderation = 0;
            for et_ex in et_exs:
                total += et_ex.cote
                sommePonderation+=et_ex.ponderation
            moyenne = (total/sommePonderation)*et_exs[0].ponderation_blobal

            row.append(moyenne)
            totalMoyenne += moyenne
            row.append(totalMoyenne)

        writer.writerow(row)
        cours.is_cote_submited = True
        cours.save()

        # Push a message on the template
        messages.success(request, 'Les cotes des étudiants ont été remis avec succès !')


    return redirect('cotes', cours_id)


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
                return redirect('cours-enseignant')

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
def cotes(request, cours_id):
    try:
        tps_count = []
        tds_count = []
        interros_count = []
        examens_count = []
        cotes_etudiant = []

        cours = Cours.objects.filter(id=cours_id)

        cotes = Cotes.objects.values('code','label','cours').annotate(dcount=Count('code')).order_by()
 

        tps = Cotes.objects.all().filter(label='TP', cours=cours_id)
        tds = Cotes.objects.all().filter(label='TD', cours=cours_id)
        interros = Cotes.objects.all().filter(label='INT', cours=cours_id)
        examens = Cotes.objects.all().filter(label='EX', cours=cours_id)


        for cote in cotes:

            if cote['cours']==cours_id and cote['label']=='TP':
                tps_count.append(cote) 
                cotes_etudiant = Cotes.objects.all().filter(code=cote['code'])
            elif cote['cours']==cours_id and cote['label']=='TD':
                tds_count.append(cote)
                cotes_etudiant = Cotes.objects.all().filter(code=cote['code'])
            elif cote['cours']==cours_id and cote['label']=='INT':
                interros_count.append(cote)
                cotes_etudiant = Cotes.objects.all().filter(code=cote['code'])
            elif cote['cours']==cours_id and cote['label']=='EX':
                examens_count.append(cote)
                cotes_etudiant = Cotes.objects.all().filter(code=cote['code'])

        pass
    except:
        messages.success(request, 'Connectez-vous avec un compte enseignant')
        return redirect('login')

    context={
        'cours':cours,
        'cotes': cotes,
        'tps_count': tps_count,
        'tds_count': tds_count,
        'interros_count': interros_count,
        'interros': interros,
        'examens_count': examens_count,
        'examens': examens,
        'cotes_etudiant': cotes_etudiant,
        'tps': tps,
        'tds': tds
    }
    return render(request, 'dashboard/pages/cotes.html', context)


@login_required
def coursEnseignant(request):
    try:
        enseignant = Enseignant.objects.get(user=request.user)
        cours = Cours.objects.filter(enseignant=enseignant)
        universites = Universite.objects.all()
        pass
    except:
        messages.success(request, 'Connectez-vous avec un compte enseignant')
        return redirect('login')

    context={
        'cours':cours,
        'universites': universites
    }
    return render(request, 'dashboard/pages/cours-enseignant.html', context)


@login_required
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


@login_required
def download_file(request, course_id):
    
    cours = Cours.objects.get(id=course_id)

    # Define text file name
    filename = f'{cours.nom_cours}.csv'
    # Define the full file path
    filepath = 'cotes/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    
    return response



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
            password = motDePasse
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
def question(request):
    return render(request, 'dashboard/pages/question.html')


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