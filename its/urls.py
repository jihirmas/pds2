from django.urls import path, register_converter
from . import views



urlpatterns = [
    path("", views.index),
    path("login/", views.CustomLoginView.as_view()),
    path("accounts/signup/", views.signup),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz-results/', views.quiz_results, name='quiz_results'),
    path('desarrollo/', views.desarrollo, name='desarrollo'),
    path('procesar_desarrollo/', views.procesar_desarrollo, name='procesar_desarrollo'),
    
    
]
