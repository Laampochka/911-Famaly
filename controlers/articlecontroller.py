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


from controlers.controller import Controller
from models.article import Article
from models.user import User

from exceptions import NotFoundException
from exceptions import UnauthorizedException


class ArticlesController(Controller):
    def index (self, request, response):
      articles = Article.find_all()
      print(articles)
      response.text = self.view.render_html('articles/index.html', 
      {
        'title': 'MVC Framework - articles',
        'h1' : 'articles on site',
        'articles' : articles,

      })

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        user = User.get_by_id(article.get_author_id())
            
        response.text = self.view.render_html('articles/view.html', 
      {
        'title': f'MVC Framework - {article.get_name()}',
        'h1' : f'article: {article.get_name()}',
        'article' : article, 
      })
    #    print(article.get_name(), article.get_text())


    def add(self, request, response):
        article = Article()
        article.set_author_id(1)
        article.set_name('New Article')
        article.set_text('mamatvoi')

        article.save()


    def delete(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException("статья не найдена")

        article.delete()
        response.status_code = 302
        response.headers = [('location', '/articles')]


    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.text = self.view.render_html('errors/404.html', {'error': "статья не найдена"})
            return

        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")


        if request.method =='POST':
            print (request.POST)
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()
            response.status_code = 302
            response.headers = [('location', f'/article/{article.get_id()}')]
            return

            
        response.text = self.view.render_html('articles/edit.html',{'title': f'Редактирование - {article.get_name()}','h1' : f'article: {article.get_name()}','article' : article})
        print(article.get_name(), article.get_text())