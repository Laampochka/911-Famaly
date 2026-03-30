from views.view import View
from controlers.controller import Controller




class SiteController(Controller):

    def index(self, request, response):
        db = Db()
        items = db.query("SELECT * FROM 'articles'")
        print(items)
        # response.text = self.view.render_html('site/index.html', {'title':'mvc Framework','h1':'Main page'})


    def about(self, request, response):
        response.text = self.view.render_html('site/about.html', {'title':'mvc Framework','h1':'Main page'})




    def hello(self,request,response,user_name):
        response.text = self.view.render_html('site/hello.html', {'title':'mvc Framework','h1':'dsds page', 'user' : user_name})
