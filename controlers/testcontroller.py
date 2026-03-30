from views.view import View
from controlers.controller import Controller

class TestController(Controller):


    def test(self, request, response):
        response.text = self.view.render_html('test/test.html', {'title':'mvc Framework','h1':'Main page'})


    def action(self, request, response):
        response.text = self.view.render_html('test/action.html', {'title':'Action','h1':'Info???'})