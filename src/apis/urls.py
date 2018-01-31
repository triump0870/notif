from django.conf.urls import include, url
from notifications import views

urlpatterns = [
    url(r'^crawl/', views.crawl, name='crawl')
]
