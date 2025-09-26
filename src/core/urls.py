from django.urls import path
from django.contrib.auth.views import LogoutView
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('terms&conditions', views.terms_conditions, name='terms_conditions'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/index.html'), name='logout'),
    path('register/', views.CustomRegisterView.as_view(),name='register'),
    path('profile/', views.UpdateProfileView.as_view(),name='profile'),
]