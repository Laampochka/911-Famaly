# from webob import Request, Response

# class API:
#     def __init__(self):
#         self.routes={}

#     def __call__(self, environ, start_response):
#         request= Request(environ)
#         # response= Response()

        
#         # response_body = ['{key}: {value}'.format(key=key, value=value) for key, value in sorted(environ.items())]
#         # response.text= '\n'.join(response_body)
#         # status = '200 OK'

#         # response.headers.add('Content-type', 'text/plain')
#              # response_body = '\n'.join(response_body)

        

#         # response_headers = [
#         #     ('Content-type', 'text/plain'),
#         # ]

#         # start_response(status, response_headers)

#         # return iter([response_body.encode('utf-8')])

#         response = self.handle_request(request)

#         return response(environ,start_response)
#     def handle_request(self, request):
#         response = Response()

#         request_url = request.environ.get("REQUEST_URI")
#         request.text = f"Ghbdtn ns pssds {request_url}"
#         return response
#     def routes(self,path):
#         def wrapper(handler):
#             self.routes[path] = handler
#             return handler
#         return wrapper

   

# app = API()

# @app.route("/home")

# def home(request, response):
#     response.text = "Halloo from home"
# @app.route("/about")
# def about(request,response):
#     response.text = "Halllo from about"

import os
import re

from webob import Request, Response
import routes
import handlers
from whitenoise import WhiteNoise
from exceptions import NotFoundException
from exceptions import UnauthorizedException
from views.view import View

class API:
    def __init__(self , static_dir="assets"): 
        self.routes = routes.routes
        self.whitenoise =WhiteNoise(self.wsgi_app, root=static_dir)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        # request = Request(environ)
        # response = self.handle_request(request)
        
        return self.whitenoise(environ, start_response)
    
    def handle_request(self, request):
        response = Response()
        try:
            result = self.find_handler_re(request_path=request.path)
            if result is  None:
                raise NotFoundException("статья не найдена")
            handler,params = result
            controller = handler[0](request)
            action = handler[1]
            action(controller,request, response, *params)
            

        except NotFoundException as e:
            response.status_code = 404
            response.text = View('default').render_html('errors/404.html',{'error' : e})
        except UnauthorizedException as e:
            response.status_code = 401
            response.text = View('default').render_html('errors/401.html',{'error' : e})

        return response
    
    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler
        # return None  # Явно возвращаем None, если обработчик не найден
    
    def find_handler_re(self, request_path):
        for path, handler in self.routes.items():
            match = re.search(path, request_path)
            if match is not None:
                return handler,match.groups()
        return None  # Явно возвращаем None, если обработчик не найден

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"
    
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

app = API()

# @app.route("/home")
# def home(request, response):
#     response.text = "Hello in main page"

# @app.route("/about")
# def about(request, response):
#     response.text = "Hello in page about"

# @app.route("/articles")
# def articles(request, response):
#     response.text = "This is page discription Buddie"


    