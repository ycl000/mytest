from django.conf.urls import url
from bootest import views
urlpatterns = [
    url(r'^index$', views.index),
    url(r'hero(\d+)$', views.hero) #     对应bootest(app)下views中的函数
]
