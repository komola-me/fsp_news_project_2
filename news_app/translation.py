from modeltranslation.translator import register, TranslationOptions, translator
from .models import News, Category

# 1st option
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

# 2nd option
# translator.register(News, NewsTranslationOptions)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )