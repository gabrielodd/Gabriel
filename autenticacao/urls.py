from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from autenticacao.forms import AuthenticationFormCustomizado

app_name = 'autenticacao'
 
urlpatterns = [
   path('login/', auth_views.LoginView.as_view(authentication_form=AuthenticationFormCustomizado), 
                                               name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout')                                               
]