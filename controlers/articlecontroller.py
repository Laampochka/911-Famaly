from views.view import View
from controlers.controller import Controller
from models.article import Article



class ArticlesController(Controller):

    def index(self, request, response):
        articles = Article.findAll(Article)
        response.text = self.view.render_html('articles/index.html', {'title':'mvc Framework','h1':'Articles'})

