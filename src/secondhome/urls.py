from django.conf.urls import url
from secondhome import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='pet-list')
]
