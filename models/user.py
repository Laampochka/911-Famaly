# from services.db import Db

from models.active_record_entity import ActiveRecordEntity
from exceptions import InvalidArgumentException
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

import re
import hashlib
import random

class User(ActiveRecordEntity):
    # __tablename__ = 'articles'
    # _id = None
    _nickname = None
    _email = None
    _is_confirmed= None
    _role = None
    _password_hash = None
    _auth_token = None
    _created_at = None

    def get_nickname(self):
        return self._nickname
    
    def get_email(self):
        return self._email

    def get_is_confirmed(self):
        return self._is_confirmed

    def get_role(self):
        return self._role

    def get_password_hash(self):
        return self._password_hash

    def get_is_confirmed(self):
        return self._is_confirmed

    def get_created_at(self):
        return self._created_at

    def set_email(self,_email):
        self._email = email

    def set_nickname(self,name):
        self._nickname = nickname

    def set_role(self,role):
        self._role = role

    def set_created_at(self,created_at):
        self._created_at = created_at

    def refresh_auth_token(self):
        self._auth_token = hashlib.sha1(random.randbytes(100)).hexdigest() + hashlib.sha1(random.randbytes(100)).hexdigest()

    def get_auth_token(self):
        return self._auth_token

    @staticmethod
    def sing_up(user_data):
        nickname = (user_data.get('nickname') or '').strip()
        email = (user_data.get('email') or '').strip()
        password = user_data.get('password') or ''

        if not nickname:
            raise InvalidArgumentException('Не передан логин')
        if re.search(r'^[a-zA-Z0-9]+$', nickname) is None:
            raise InvalidArgumentException('Логин: только латиница и цифры')
        if User.find_one_by_column('nickname', nickname):
            raise InvalidArgumentException('Логин уже занят')

        if not email:
            raise InvalidArgumentException('Не передан email')
        try:
            validate_email(email)
        except EmailNotValidError:
            raise InvalidArgumentException('Некорректный email')
        if User.find_one_by_column('email', email):
            raise InvalidArgumentException('Email уже занят')

        if len(password) < 8:
            raise InvalidArgumentException('Пароль минимум 8 символов')

        user = User()
        user._nickname = nickname
        user._email = email
        user._is_confirmed = True
        user._role = 'user'
        user._password_hash = generate_password_hash(password)
        user.refresh_auth_token()
        user.save()
        return user



    @staticmethod
    def sing_in(user_data):
        nickname = (user_data.get('nickname') or '').strip()
        password = user_data.get('password') or ''

        if not nickname:
            raise InvalidArgumentException('Не передан логин')

        if not re.search(r'^[a-zA-Z0-9]+$', nickname):
            raise InvalidArgumentException('Логин: только латиница и цифры')

        user = User.find_one_by_column('nickname', nickname)
        if user is None:
            raise InvalidArgumentException('Неверный логин или пароль')

        from werkzeug.security import check_password_hash
        if not check_password_hash(user.get_password_hash(), password):
            raise InvalidArgumentException('Неверный логин или пароль')

        user.refresh_auth_token()
        user.save()
        return user

    @staticmethod
    def _read_auth_fields(request):
        if request.content_type == 'application/json':
            data = request.json or {}
            return {
                'nickname': (data.get('nickname') or '').strip(),
                'password': data.get('password') or '',
            }
        return {
            'nickname': (request.POST.get('nickname') or '').strip(),
            'password': request.POST.get('password') or '',
        } 



    @staticmethod
    def get_table_name():
        return 'users'
















