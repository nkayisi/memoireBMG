from django.shortcuts import render




def accueil(request):
    return render(request, 'dashboard/pages/index.html')



def cotes(request):
    return render(request, 'dashboard/pages/cotes.html')



def enseignant(request):
    return render(request, 'dashboard/pages/enseignant.html')



def etudiant(request):
    return render(request, 'dashboard/pages/etudiant.html')



def universite(request):
    return render(request, 'dashboard/pages/universite.html')



def profile(request):
    return render(request, 'dashboard/pages/profile.html')