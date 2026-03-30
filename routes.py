# from  handlers import home, about, articles
from controlers.sitecontroller import SiteController

from controlers.testcontroller import TestController

from controlers.articlecontroller import ArticlesController

routes = {
    "/articles":[ArticlesController, ArticlesController.index],

    "/home":[SiteController, SiteController.index],
    "/about":[SiteController, SiteController.about],
    r"^/hello/(.*)$":[SiteController, SiteController.hello],

    "/test":[TestController, TestController.test],
    "/action":[TestController, TestController.action],
}