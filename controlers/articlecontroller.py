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


class ArticlesController(Controller):
    def index (self, request, response):
      articles = Article.find_all()
      print(articles)
      response.text = self.view.render_html('articles/index.html', 
      {
        'title': 'MVC Framework - articles',
        'h1' : 'articles on site',
        'articles' : articles
      })

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.text = self.view.render_html('errors/404.html', {'error': "статья не найдена"})
            return
        response.text = self.view.render_html('articles/view.html', 
      {
        'title': f'MVC Framework - {article.get_name()}',
        'h1' : f'article: {article.get_name()}',
        'article' : article
      })
    #    print(article.get_name(), article.get_text())


    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.text = self.view.render_html('errors/404.html', {'error': "статья не найдена"})
            return
        if request.method =='POST':
            print (request.POST)
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()

            
        response.text = self.view.render_html('articles/edit.html',{'title': f'Редактирование - {article.get_name()}','h1' : f'article: {article.get_name()}','article' : article})
        print(article.get_name(), article.get_text())