from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Journalist, Category, NewsPortal, PortalCategory,
    NewsArticle, User, Comment, Subscription, Advertisement
)


admin.site.unregister(AuthUser)

@admin.register(AuthUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'date_joined')
    list_editable = ('is_staff',)
    list_filter = ('is_staff', 'is_superuser')

@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')
    search_fields = ('name', 'email', 'user__username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(NewsPortal)
class NewsPortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(PortalCategory)
class PortalCategoryAdmin(admin.ModelAdmin):
    list_display = ('portal', 'category')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_by', 'published_date', 'views')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    readonly_fields = ('views', 'published_date')


@admin.register(User)
class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('content',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'start_date', 'end_date')
    list_filter = ('plan_type',)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('advertiser_name', 'start_date', 'end_date', 'created_by')
    search_fields = ('advertiser_name',)