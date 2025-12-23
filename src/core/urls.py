from django.urls import path
from django.contrib.auth.views import LogoutView
from core import views

from .views import (
    PetListView,
    PetDetailView,
    PetCreateView,
    PetUpdateView,
    PetDeleteView,
)

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('terms&conditions', views.terms_conditions, name='terms_conditions'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/index.html'), name='logout'),
    path('register/', views.CustomRegisterView.as_view(),name='register'),
    path('profile/', views.UpdateProfileView.as_view(),name='profile'),
    path('list', PetListView.as_view(), name='list'),
    path('<int:pk>/', PetDetailView.as_view(), name='detail'),
    path('create/', PetCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PetUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PetDeleteView.as_view(), name='delete'),
]