from about import views
from django.urls import path

urlpatterns = [
    path('author/', views.AboutView.as_view()),
    path('spec/', views.SpecView.as_view()),
]
