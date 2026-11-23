from models.article import Article
from controlers.controller import Controller
from exceptions import NotFoundException
from exceptions import UnauthorizedException
from exceptions import InvalidMethodException
from exceptions import ForbiddenException 
from models.user import User 
import json


class ArticlesApiController(Controller):

    def index(self, request, response):
        articles = Article.find_all()
        response.text = self.view.render_html('api/articles.html', {
            'title': 'Все статьи',
            'articles': articles,
        })

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")
        response.text = self.view.render_html('api/article.html', {
            'title': f'Article: {article.get_name()}',
            'article': article,
        })
    def cards(self, request, response):
        articles = Article.find_all()
        response.text = self.view.render_html('api/articles.html', {
            'title': 'Все статьи',
            'articles': articles,
        })

    
    def _json(self, response, data, status=200):        # ← 4 пробела (метод класса)
        response.status_code = status
        response.content_type = 'application/json'
        response.text = json.dumps(data, ensure_ascii=False, default=str)

    def _ensure_can_modify(self, article):              # ← 4 пробела (метод класса)
        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")
        if (article.get_author_id() != self.user.get_id()
                and self.user.get_role() != 'admin'):
            raise ForbiddenException("Нет прав на изменение этой статьи")




    def _extract_fields(self, request):
        if request.content_type == 'application/json':
            data = request.json or {}
            if 'articles' in data and isinstance(data['articles'], list) and data['articles']:
                data = data['articles'][0]
            return {
                'name': (data.get('name') or '').strip(),
                'text': (data.get('text') or '').strip(),
            }, None

        fields = {
            'name': (request.POST.get('name') or '').strip(),
            'text': (request.POST.get('text') or '').strip(),
        }
        img_file = request.POST.get('img')
        if img_file is not None and not getattr(img_file, 'filename', ''):
            img_file = None
        return fields, img_file

    def _resolve_author(self):
        """Автор: залогиненный пользователь, иначе — первый/любой из БД."""
        if self.user is not None:
            return self.user

        users = User.find_all()
        if users:
            return users[0]

        # в БД вообще нет пользователей — создаём технического
        u = User()
        u._nickname = 'anonymous'
        u._email = 'anonymous@local'
        u._is_confirmed = True
        u._role = 'admin'
        u._password_hash = '!'
        u.refresh_auth_token()
        u.save()
        return u

    def add(self, request, response):
        print('ADD: self.user =', self.user)               # отладка

        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")

        fields, img_file = self._extract_fields(request)
        if not fields['name']:
            return self._json(response, {'error': 'не передано название статьи'}, 422)

        try:
            article = Article.create(fields, img_file, self.user)   # ← self.user
        except UnauthorizedException as e:
            return self._json(response, {'error': str(e)}, 401)
        except InvalidArgumentException as e:
            return self._json(response, {'error': str(e)}, 422)    

        return self._json(response, {'article': article.to_dict()}, 201)

    def update(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        # self._ensure_can_modify(article)              # ← IDOR-проверка

        name = (request.POST.get('name') or '').strip()
        text = (request.POST.get('text') or '').strip()

        if not name:
            return self._json(response, {'error': 'не передано название статьи'}, 422)
        if not text:
            return self._json(response, {'error': 'не передан текст статьи'}, 422)

        article.set_name(name)
        article.set_text(text)

        # новое изображение (необязательно)
        img_file = request.POST.get('img')
        if img_file is not None and getattr(img_file, 'filename', ''):
            if not Article.check_file_extension(img_file.filename):
                return self._json(response, {'error': 'Недопустимый формат. Разрешены: png, jpg, jpeg, gif, webp'}, 422)
            if not Article.check_file_mime(img_file):
                return self._json(response, {'error': 'Файл не является изображением'}, 422)
            ok, _ = Article.check_file_size(img_file, MAX_FILE_SIZE)
            if not ok:
                return self._json(response, {'error': f'Файл больше {MAX_FILE_SIZE // (1024 * 1024)} МБ'}, 422)

            safe_name = Article.generate_safe_filename(img_file.filename)
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, safe_name)

            img_file.file.seek(0)
            with open(file_path, 'wb') as f:
                while True:
                    chunk = img_file.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

            article._img = 'uploads/' + safe_name

        article.save()
        return self._json(response, {'article': article.to_dict()}, 200)

    def delete(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.content_type = 'application/json'
            response.text = json.dumps(
                {'error': 'статья не найдена'},
                ensure_ascii=False,
            )
            return

        article_id = article.get_id()
        article.delete()

        response.status_code = 200
        response.content_type = 'application/json'
        response.text = json.dumps(
            {'ok': True, 'id': article_id},
            ensure_ascii=False,
        )