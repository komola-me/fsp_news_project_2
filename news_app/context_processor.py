from .models import News, Category

def latest_news_top(request):
    latest_news_top = News.published.all().order_by('-published_time')[:10]
    categories = Category.objects.all()

    context = {
        'latest_news_top': latest_news_top,
        'categories': categories,
    }

    return context
