from msilib.schema import ListView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import News, Category, Contact
from django.db import models
from .forms import ContactForm
from django.views.generic import TemplateView, ListView

# Create your views here.
def news_list(request):
    # news_list = News.objects.all()
    news_list = News.published.all()
    # news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }

    return render(request, 'news/news_detail.html', context)


def homePageView(request):
    news_list = News.published.all().order_by('-published_time')
    categories = Category.objects.all()

    latest_news = News.published.all().order_by('-published_time')[:5]

    # local_news_main = News.published.filter(category__name="Local").order_by('-published_time')[:1]
    # local_news_list = News.published.all().filter(category__name="Local").order_by('-published_time')[1:6]
    local_news_list = News.published.all().filter(category__name="Local").order_by('-published_time')[:5]

    context = {
        "news_list": news_list,
        "categories": categories,
        "latest_news": latest_news,
        # "local_news_main": local_news_main,
        # "local_news_list": local_news_list,
        "local_news_list": local_news_list,
    }

    return render(request, 'news/index.html', context)


def contactPageView(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse("<h2> Thank you for contacting with us")

    context = {
        "form": form
    }

    return render(request, 'news/contact.html', context)


def aboutPageView(request):

    context = {
    }

    return render(request, 'news/about.html', context)


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Thank you for contacting us")
        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)


class HomePageView(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["news_list"] = News.published.all().order_by('-published_time')[:15]
        context["latest_news"] = News.published.all().order_by('-published_time')[:5]
        # context["local_news_main"] = News.published.filter(category__name="Local").order_by('-published_time')[:1]
        # context["local_news_list"] = News.published.all().filter(category__name="Local").order_by('-published_time')[1:6]
        context["local_news_list"] = News.published.filter(category__name="Local").order_by('-published_time')[:5]

        context["world_news_list"] = News.published.filter(category__name="World").order_by('-published_time')[:5]
        context["tech_news_list"] = News.published.filter(category__name="Tech").order_by('-published_time')[:5]
        context["sport_news_list"] = News.published.filter(category__name="Sport").order_by('-published_time')[:5]

        return context


class LocalNewsListView(ListView):
    model = News
    template_name = "news/local.html"
    context_object_name = "local_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Local')
        return news



class WorldNewsListView(ListView):
    model = News
    template_name = "news/world.html"
    context_object_name = "world_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='World')
        return news


class TechNewsListView(ListView):
    model = News
    template_name = "news/tech.html"
    context_object_name = "tech_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Technology')
        return news


class SportNewsListView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = "sport_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news