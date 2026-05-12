from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_not_required # type:ignore
from django.contrib.auth import update_session_auth_hash, login
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pet
from .forms import CustomAuthenticationForm, CustomCreationForm, UserProfileForm, PetForm


@login_not_required
def index(request):
    return render(request, "core/index.html")

@login_not_required
def terms_conditions(request):
    return render(request, "core/terms_conditions.html")

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'core/login.html'
    next_page = reverse_lazy('core:index')

    def form_valid(self, form: AuthenticationForm):
        user = form.get_user()
        messages.success(self.request, f"Hola de nuevo {user.username}")
        return super().form_valid(form)


@method_decorator(login_not_required, name='dispatch')
class CustomRegisterView(CreateView):
    form_class = CustomCreationForm
    template_name = "core/register.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UpdateProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "core/profile.html"
    success_url = reverse_lazy("core:index")

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, "Perfil actualizado correctamente")
        return response


class PetListView(ListView):
    model = Pet
    template_name = "core/pet_list.html"
    context_object_name = "pets"
    paginate_by = 12


class PetDetailView(DetailView):
    model = Pet
    template_name = "core/pet_detail.html"
    context_object_name = "pet"


class PetCreateView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = "core/pet_form.html"
    success_url = reverse_lazy("core:list")


class PetUpdateView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "core/pet_form.html"
    success_url = reverse_lazy("core:list")


class PetDeleteView(DeleteView):
    model = Pet
    template_name = "core/pet_confirm_delete.html"
    success_url = reverse_lazy("core:list")