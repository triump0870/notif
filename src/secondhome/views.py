from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = 'app.html'
