# from views.view import View
# from controlers.controller import Controller
# from models.article import Article



# class ArticlesController(Controller):

#     def index(self, request, response):
#         articles = Article.find_all(Article)
#         response.text = self.view.render_html('articles/index.html', {'title': f'mvc Framework - {Article.name}','h1': f'Articles: {Article.id}','articles':articles})

#     def view(self, request, response, id):
#         articles = Article.get_by_id(id, Article)
#         # print(article)

import cgi
from controlers.controller import Controller
from models.article import Article, InvalidArgumentException
from models.user import User

import secrets
import string
from exceptions import ForbiddenException 

from exceptions import NotFoundException
# from exceptions import InvalidArgumentException
from exceptions import UnauthorizedException


class ArticlesController(Controller):
    def ensure_can_modify(self, article):
        """Разрешает изменять статью только автору или админу."""
        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")

        is_author = article.get_author_id() == self.user.get_id()
        is_admin = self.user.get_role() == 'admin'

        if not (is_author or is_admin):
            raise ForbiddenException("Нет прав на изменение этой статьи")

    def index(self, request, response):

        users = User.find_all()
        response.text = self.view.render_html('users/users.html', {
            'title': 'MVC Framework - users',
            'users': users,
        })
            
    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        response.text = self.view.render_html('articles/view.html', {
            'title': f'MVC Framework - {article.get_name()}',
            'h1': f'article: {article.get_name()}',
        })
    #    print(article.get_name(), article.get_text())


    def get_form(self, request):
        return cgi.FieldStorage(
            fp=request.environ['wsgi.input'],

            environ=request.environ,
        )

    # def check_csrf(self, request, form):

    #     form.getvalue('csrf_token')
    #     token_from_form = request.form.get('token')
    #     token_from_sess = request.session.get('csrf_token')
    #     return token_from_sess and tokenfrom_form == token_from_sess

    # def issue_csrf(self, request):

    #     token = secrets.token_urlsafe(32)
    #     request.session['csrf_token'] = token
    #     request.session.dirty = True
    #     return token
    def add(self, request, response):
        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")

        if request.method == 'POST':
            fields = {'name': '', 'text': ''}
            try:
                form = cgi.FieldStorage(
                    fp=request.environ['wsgi.input'],
                    environ=request.environ,
                    keep_blank_values=True,
                )

                fields = {
                    'name': (form.getvalue('name') or '').strip(),
                    'text': (form.getvalue('text') or '').strip(),
                }

                # поле img может отсутствовать — берём аккуратно
                img_file = form['img'] if 'img' in form else None
                if img_file is not None and not getattr(img_file, 'filename', ''):
                    img_file = None

                article = Article.create(fields, img_file, self.user)

                response.status_code = 302
                response.headers.append(('Location', '/articles'))
                return

            except InvalidArgumentException as e:
                response.text =  self.view.render_html(
                    'articles/add.html',
                    {
                        'title': 'MVC Framework - Add article',
                        'article_data': fields,
                        'error': str(e),
                    },
                )
                return

        response.text =  self.view.render_html(
            'articles/add.html',
            {'title': 'Add article'},
        )

    # def add(self, request, response):
    #     if self.user is None:
    #         raise UnauthorizedException("Необходимо авторизоваться")

    #     if request.method == 'POST':
    #         try:
    #             form = cgi.FieldStorage(fp=request.environ['wsgi.input'], environ=request.environ)
    #             fields = {
    #                 'name' : form.getvalue('name'),
    #                 'text' : form.getvalue('text')
    #             }
    #             img_file = form['img']
    #             article = Article.create(fields, img_file, self.user)
    #             if isinstance(article, Article):
    #                 response.status_code = 302
    #                 response.headers = [('Location', '/articles')]
    #                 return
                
    #         except InvalidArgumentException as e:
    #             response.text = self.view.render_html('articles/add.html', 
    #             {
    #             'title': 'MVC Framework - Add article',
    #             'article_data' : fields,
    #             'error': e
    #             })
    #             return

    #     response.text = self.view.render_html('articles/add.html', {'title' : 'Add article'})

        # article = Article()
        # article.set_author_id(1)
        # article.set_name('New Article')
        # article.set_text('mamatvoi')

        # article.save()


    # def delete(self, request, response, id):
    #     article = Article.get_by_id(id)
    #     if article is None:
    #         raise NotFoundException("статья не найдена")

    #     article.delete()
    #     response.status_code = 302
    #     response.headers = [('location', '/articles')]


    def search(self,request,response):
        if not 'q' in request.GET:
            response.text = self.view.render_html('articles/search.html')
            return
        else:
            articles = Article.search_by_name(request.GET['q'])
            response.text = self.view.render_html('articles/search.html', {'q' : request.GET['q'], 'articles' : articles})


    # def edit(self, request, response, id):
    #     article = Article.get_by_id(id)
    #     if article is None:
    #         response.status_code = 404
    #         response.text = self.view.render_html('errors/404.html', {'error': "статья не найдена"})
    #         return

    #     if self.user is None:
    #         raise UnauthorizedException("Необходимо авторизоваться")


    #     if request.method =='POST':
    #         print (request.POST)
    #         article.set_name(request.POST['name'])
    #         article.set_text(request.POST['text'])
    #         article.save()
    #         response.status_code = 302
    #         response.headers = [('location', f'/article/{article.get_id()}')]
    #         return

    #     # token = self.issue_csrf(request)
    #     # response.text = self.view.render_html('articles/edit.html', {
    #     # 'title': f'Редактирование - {article.get_name()}',
    #     # 'article': article,
    #     # 'csrf_token': token,
    #     # })

            
    #     response.text = self.view.render_html('articles/edit.html',{'title': f'Редактирование - {article.get_name()}','h1' : f'article: {article.get_name()}','article' : article})
    #     print(article.get_name(), article.get_text())



    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        self.ensure_can_modify(article)   # ✅ проверка владельца

        if request.method == 'POST':
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()
            response.status_code = 302
            response.headers = [('location', f'/article/{article.get_id()}')]
            return

        response.text = self.view.render_html('articles/edit.html', {...})

    def delete(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        self.ensure_can_modify(article)   # ✅ проверка владельца

        article.delete()
        response.status_code = 302
        response.headers = [('location', '/articles')]


