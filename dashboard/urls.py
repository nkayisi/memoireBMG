from django.urls import path


from . import views as dashboardViews





urlpatterns = [
    path('nouvelle-cote', dashboardViews.nouvelle_cote, name='nouvelle_cote'),

    path('', dashboardViews.accueil, name="accueil"),
    path('login/', dashboardViews.loginView, name="login"),   
    path('cotes/', dashboardViews.cotes, name="cotes"),
    path('enseignant/', dashboardViews.enseignant, name="enseignant"),
    path('etudiant/', dashboardViews.etudiant, name="etudiant"),
    path('universite/', dashboardViews.universite, name="universite"),
    path('profile/', dashboardViews.profile, name="profile"),
    path('cours/', dashboardViews.cours, name="cours"),

    path('logout/', dashboardViews.logOut, name="logout"),
    path('cotes/js/', dashboardViews.SomeFunction, name="cjs"),
    path('download/csv/<str:course_id>/', dashboardViews.download_csv, name="download"),
]
