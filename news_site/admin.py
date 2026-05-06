from django.contrib import admin
from .models import (
    Admin, User, Journalist, Category,
    NewsPortal, PortalCategory, NewsArticle,
    Comment, Subscription, Advertisement,
)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'views')
    list_filter = ('category', 'author', 'published_date')
    search_fields = ('title', 'content')
    ordering = ('-published_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'start_date', 'end_date')
    list_filter = ('plan_type',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('advertiser_name', 'start_date', 'end_date', 'created_by')
    list_filter = ('start_date', 'end_date')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(NewsPortal)
class NewsPortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(PortalCategory)
class PortalCategoryAdmin(admin.ModelAdmin):
    list_display = ('portal', 'category')
