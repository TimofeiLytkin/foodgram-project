from django.urls import path

from . import views

urlpatterns = [
    path("v1/ingredients/", views.IngredientAPIView.as_view()),
    path("v1/favorites/", views.FavoriteCreateView.as_view()),
    path("v1/favorites/<int:id>/", views.FavoriteDeleteView.as_view()),
    path("v1/purchases/", views.PurchaseCreateView.as_view()),
    path("v1/purchases/<int:id>/", views.PurchaseDeleteView.as_view()),
    path("v1/subscriptions/", views.SubscribeCreateView.as_view()),
    path("v1/subscriptions/<int:id>/", views.SubscribeDeleteView.as_view()),
]
