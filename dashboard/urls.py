from django.urls import path


from . import views as dashboardViews





urlpatterns = [
    path('nouvelle-cote/<cours_id>', dashboardViews.nouvelle_cote, name='nouvelle_cote'),

    path('', dashboardViews.accueil, name="accueil"),
    path('login/', dashboardViews.loginView, name="login"), 
    path('cours-enseignant/', dashboardViews.coursEnseignant, name="cours-enseignant"),

    path('question/', dashboardViews.question, name="question"),

    path('cotes/<int:cours_id>/', dashboardViews.cotes, name="cotes"),
    path('cotes/ajax/', dashboardViews.coter, name="ajax"),
    path('envoie-cotes/<int:cours_id>/', dashboardViews.envoieCotes, name="envoi-cotes"),

    path('enseignant/', dashboardViews.enseignant, name="enseignant"),
    path('etudiant/', dashboardViews.etudiant, name="etudiant"),
    path('universite/', dashboardViews.universite, name="universite"),
    path('profile/', dashboardViews.profile, name="profile"),
    path('cours/', dashboardViews.cours, name="cours"),

    path('logout/', dashboardViews.logOut, name="logout"),
    path('cotes/js/', dashboardViews.SomeFunction, name="cjs"),
    path('download/csv/<str:course_id>/', dashboardViews.download_csv, name="download"),

    path('download/<str:course_id>/', dashboardViews.download_file, name="dwnl"),
]
