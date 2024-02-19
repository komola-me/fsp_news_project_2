from msilib.schema import ListView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import News, Category, Contact, Comment
from django.db import models
from .forms import CommentForm, ContactForm
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.db.models import Q
from hitcount.views import HitCountDetailView

# Create your views here.
def news_list(request):
    # news_list = News.objects.all()
    news_list = News.published.all()
    # news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)


class NewsDetailView(HitCountDetailView, DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = 'news'
    slug_url_kwarg = 'news' # the name of the URL keyword argument used to retrieve the news object.
    count_hit = True



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_count'] = self.object.comments.filter(active=True).count()
        # news = self.object
        # news.view_count = news.view_count + 1
        # news.save()
        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = self.object
            new_comment.user = request.user
            new_comment.save()
            return self.render_to_response(self.get_context_data(comment_form=CommentForm()))
        else:
            return self.render_to_response(self.get_context_data(comment_form=comment_form))


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    comments = news.comments.filter(active=True)
    # news.view_count = news.view_count + 1
    # news.save()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #new comment object will be created but not saved to db
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            #malumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    context = {
        "news": news,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }

    return render(request, 'news/news_detail.html', context)

@login_required
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
        news = self.model.published.all().filter(category__name='Tech')
        return news


class SportNewsListView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = "sport_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status', )
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

    # def your_view(request):
    #     News.slug = slugify(['title'])
    #     News.save()

@user_passes_test(lambda u:u.is_superuser)
@login_required
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        "admin_users": admin_users,
        }

    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'results_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)
            )