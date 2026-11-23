from views.view import View
from controlers.controller import Controller
from services.db import Db
from models.article import Article



class SiteController(Controller):

    def index(self, request, response):
        response.text = self.view.render_html('api/index.html', {
            'title': 'mvc Framework - API docs',
            'h1': 'API documentation',
        })


    def about(self, request, response):
        response.text = self.view.render_html('site/about.html', {'title':'mvc Framework','h1':'Main page'})




    def hello(self,request,response,user_name):
        response.text = self.view.render_html('site/hello.html', {'title':'mvc Framework','h1':'dsds page', 'user' : user_name})
