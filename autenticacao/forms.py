from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import PasswordInput

class AuthenticationFormCustomizado(AuthenticationForm):

   error_messages = {
      'invalid_login': 'Login inválido',
   }

   username = forms.CharField(
      error_messages={'required': 'Campo obrigatório.', },
      widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '25'}),
      required=True)
   
   # <input type='text'
   #        name='username'
   #        id='id_username'
   #        class='form-control form-control-sm'
   #        maxlength='25'
   #        required>

   password = forms.CharField(
      error_messages={'required': 'Campo obrigatório.', },
      widget=PasswordInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '25'}),
      required=True)
   
   # <input type='password'
   #        name='password'
   #        id='id_password'
   #        class='form-control form-control-sm'
   #        maxlength='25'
   #        required>
