from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Categories
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Main'
        context['content'] = "Online Store of Electronics!"
        context['categories'] = Categories.objects.all()
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - About Us'
        context['content'] = "Welcome to our online shop!"
        return context

# def index(request):
#     categories = Categories.objects.all()
#
#     context = {
#         'title': 'Home - Главная',
#         'content': "Welcome to our online shop",
#
#     }
#
#     return render(request, 'main/index.html', context)

# def about(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': "О нас",
#         'text_on_page': "Текст о том почему этот магазин такой классный, и какой хороший товар."
#     }
#
#     return render(request, 'main/about.html', context)