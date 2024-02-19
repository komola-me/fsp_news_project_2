from django.contrib import admin
from .models import News, Category, Contact, Comment

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

# 2nd option
# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)

# 1st option
admin.site.register(Comment, CommentAdmin)