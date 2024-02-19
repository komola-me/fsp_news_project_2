from django.urls import path
from .views import news_list, news_detail, homePageView, contactPageView, aboutPageView, ContactPageView, HomePageView, LocalNewsListView, WorldNewsListView, TechNewsListView, SportNewsListView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view, NewsDetailView, SearchResultsList

urlpatterns = [
    # path('', homePageView, name='home_page'),
    path('', HomePageView.as_view(), name='home_page'),
    path('all/', news_list, name='all_news_list'),
    path('adminpage/', admin_page_view, name="admin_page"),

    path('searchresults/', SearchResultsList.as_view(), name="search_results"),


    path('local/', LocalNewsListView.as_view(), name="local_news_page"),
    path('world/', WorldNewsListView.as_view(), name="world_news_page"),
    path('tech/', TechNewsListView.as_view(), name="tech_news_page"),
    path('sport/', SportNewsListView.as_view(), name="sport_news_page"),

    path('create/', NewsCreateView.as_view(), name='news_create'),
    # path('<slug:news>/', news_detail, name='news_detail_page'),
    path('<slug:news>/', NewsDetailView.as_view(), name='news_detail_page'),
    path('<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),

    path('about', aboutPageView, name='about_page'),
    # path('contact-us', contactPageView, name='contact_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),




]
