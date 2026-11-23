from views.view import View
from models.user_auth_service import UserAuthService
from exceptions import UnauthorizedException

class ApiController:
    def __init__(self, request):
        token = request.cookies['token'] if 'token' in request.cookies else ''
        self.user = UserAuthService.get_user_by_token(token)



class Controller:
    # def __init__(self, request):
    #     self.layout="default"
    #     self.view =  View(self.layout)
    #     token = request.cookies['token'] if'token' in request.cookies else ''
    #     self.user = UserAuthService.get_user_by_token(token)
    #     self.view.set_var('user',self.user)

    def __init__(self, request):
        self.layout = "default"
        self.view = View(self.layout)

        # 1) cookie token
        token = request.cookies.get('token', '')
        self.user = UserAuthService.get_user_by_token(token)

        # 2) Basic (если cookie не дала)
        if self.user is None:
            auth = request.headers.get('Authorization')
            # может бросить UnauthorizedException — пробрасываем,
            # handle_request отдаст 401 + WWW-Authenticate
            self.user = UserAuthService.getUserByAuthBasic(auth)

        self.view.set_var('user', self.user)