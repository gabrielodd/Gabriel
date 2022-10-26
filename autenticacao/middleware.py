from django.http import HttpResponseRedirect
from projeto import settings

class LoginRequiredMiddleware:
   def __init__(self, get_response):
      self.get_response = get_response
      self.login_path = getattr(settings, 'LOGIN_URL')
   
      print('init - get_response = ', get_response)
      print('init - login_path = ', self.login_path)
   
      # init - get_response =  <function BaseHandler._get_response at 0x0000023F187A2488>
      # init - login_path =  /autenticacao/login/
   def __call__(self, request):
      # Code to be executed for each request before
      # the view (and later middleware) are called.
   
      print('request.path = ', request.path)
      print('self.login_path = ', self.login_path)
      print('request.user.is_anonymous = ', request.user.is_anonymous)
   
      if request.path != self.login_path and request.user.is_anonymous:
         return HttpResponseRedirect('%s?next=%s' % (self.login_path, request.path))
   
      response = self.get_response(request)
   
      # Code to be executed for each request/response after
      # the view is called.
   
      return response
   
   # class A:
   #    def __init__(self):
   #       print('init')
   #    def __call__(self):
   #       print('call')
   #
   # a = A() ==> provoca a execução do método init
   # a()     ==> provoca a execução do método call (o objeto é chamado como uma função)
   #    