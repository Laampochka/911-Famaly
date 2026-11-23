# from  handlers import home, about, articles
from controlers.sitecontroller import SiteController

from controlers.testcontroller import TestController

from controlers.articlecontroller import ArticlesController

from controlers.api.articleapicontroller import ArticlesApiController

from controlers.users_controller import UsersController

routes = {



    r'^/article/(\d+)/edit$':[ArticlesController, ArticlesController.edit],
    r'^/article/(\d+)$':[ArticlesController, ArticlesController.view],
    r'^/article/(\d+)/delete$':[ArticlesController, ArticlesController.delete],
    r'^/articles/add$':[ArticlesController, ArticlesController.add],
    r'^/articles/search$':[ArticlesController, ArticlesController.search],
    
    # r'^/api/articles$': [ArticlesApiController, ArticlesApiController.index],

    r'^/api/article/(\d+)$':[ArticlesApiController, ArticlesApiController.view],
    r'^/api/docs$':[SiteController, SiteController.index],
    r'^/api/articles/?$': [ArticlesApiController, {'GET': ArticlesApiController.cards, 'POST': ArticlesApiController.add}],
    
    r'^/api/article/(\d+)/update$': [ArticlesApiController, {'POST': ArticlesApiController.update}],
    r'^/api/article/(\d+)/delete$': [ArticlesApiController, {'POST': ArticlesApiController.delete}],
    
    # '/articles':[ArticlesController, ArticlesController.index],

    r'^/user/register$':[UsersController, UsersController.sing_up],
    r'^/user/login$':[UsersController, UsersController.sing_in],
    r'^/user/logout$':[UsersController, UsersController.logout],
    r'^/user/users$':[UsersController, UsersController.index],
    

    "/home":[SiteController, SiteController.index],
    "/about":[SiteController, SiteController.about],
    r"^/hello/(.*)$":[SiteController, SiteController.hello],

    "/test":[TestController, TestController.test],
    "/action":[TestController, TestController.action],
}