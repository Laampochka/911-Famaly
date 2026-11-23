from models.user import User
import base64
import binascii
from exceptions import UnauthorizedException   
from werkzeug.security import check_password_hash   



class UserAuthService():
    @staticmethod
    def create_token(user):
        return str(user.get_id()) + ':' + user.get_auth_token()

    @staticmethod
    def get_user_by_token(token):
        if token == '':
            return None
        
        [user_id, auth_token] = token.split(':', 2)
        user = User.get_by_id(int(user_id))
        if user is None:
            return None
        if user.get_auth_token() != auth_token:
            return None
        return user


    @staticmethod
    def getUserByAuthBasic(authorization_header):
        if not authorization_header:
            return None                                        # заголовка нет

        parts = authorization_header.split(' ', 1)
        if len(parts) != 2 or parts[0].lower() != 'basic':
            raise UnauthorizedException("Требуется Basic-аутентификация")

        try:
            decoded = base64.b64decode(parts[1], validate=True).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError, ValueError):
            raise UnauthorizedException("Некорректный Basic-заголовок")

        if ':' not in decoded:
            raise UnauthorizedException("Некорректный Basic-заголовок")

        login, password = decoded.split(':', 1)
        if not login or not password:
            raise UnauthorizedException("Некорректный Basic-заголовок")

        user = User.find_one_by_column('nickname', login)
        if user is None:
            raise UnauthorizedException("Неверный логин или пароль")

        if not check_password_hash(user.get_password_hash(), password):
            raise UnauthorizedException("Неверный логин или пароль")

        return user