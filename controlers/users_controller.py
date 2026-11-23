

from controlers.controller import Controller
from models.user import User

from exceptions import NotFoundException
from exceptions import InvalidArgumentException
from models.user_auth_service import UserAuthService


class UsersController(Controller):




    
    def sing_up (self, request, response):

        if request.method == 'POST':
            try:
                user = User.sing_up(request.POST)
                if isinstance(user, User):
                    response.text = self.view.render_html('users/singUpSuccess.html',{})
                    return
                
            except InvalidArgumentException as e:
                response.text = self.view.render_html('users/sing_up.html', 
                {
                'title': 'MVC Framework - Sing up',
                'user_data' : request.POST,
                'error': e
                })
                return


        response.text = self.view.render_html('users/sing_up.html', 
        {
        'title': 'MVC Framework - Sing up',
        })

    def sing_in(self, request, response):
        if request.method == 'POST':
            data = User._read_auth_fields(request)     # ← вместо ручного dict
            print('data:', data)                        # можно оставить для отладки
            try:
                user = User.sing_in(data)
                if isinstance(user, User):
                    token = UserAuthService.create_token(user)
                    response.set_cookie(
                        'token', token,
                        max_age=86400,
                        path='/',
                        httponly=True,
                        samesite='Lax',
                    )
                    response.status_code = 302
                    response.location = '/api/articles'
                    return
                response.text = self.view.render_html('users/sing_in.html', {
                    'title': 'MVC Framework - Sing in',
                    'user_data': data,
                    'error': 'Неверный логин или пароль',
                })
                return
            except InvalidArgumentException as e:
                response.text = self.view.render_html('users/sing_in.html', {
                    'title': 'MVC Framework - Sing in',
                    'user_data': data,
                    'error': e,
                })
                return

        response.text = self.view.render_html('users/sing_in.html', {
            'title': 'MVC Framework - Sing in',
        })

    def logout(self, request, response):
        response.set_cookie('token', '', -1, '/')
        response.status_code = 302
        response.location = request.referer
        
    def index (self, request, response):
      users = User.find_all()
      print(users)
      response.text = self.view.render_html('users/users.html', 
      {
        'title': 'MVC Framework - users',
        'h1' : 'articles on site',
        'user_data' : request.POST,

      })