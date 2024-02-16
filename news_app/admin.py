from django.contrib import admin
from .models import News, Category, Contact

# Register your models here.
# admin.site.register(News)
# admin.site.register(Category)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_time', 'status']
    list_filter = ['status', 'created_time', 'published_time']
    prepopulated_fields = {"slug": ('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['status', 'published_time']


# @admin.register(Category)
# class Category(admin.ModelAdmin):
#     list_display = ['id', 'name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Category, CategoryAdmin)


admin.site.register(Contact)