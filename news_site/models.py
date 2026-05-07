from django.db import models
from django.contrib.auth.models import User as AuthUser


class Admin(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'admins'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Journalist(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'journalists'
        verbose_name = 'Journalist'
        verbose_name_plural = 'Journalists'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class NewsPortal(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'news_portal'
        verbose_name = 'News Portal'
        verbose_name_plural = 'News Portals'


class PortalCategory(models.Model):
    portal = models.ForeignKey(NewsPortal, on_delete=models.CASCADE, related_name='portal_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='portal_categories')

    class Meta:
        db_table = 'portal_categories'
        unique_together = ('portal', 'category')
        verbose_name = 'Portal Category'
        verbose_name_plural = 'Portal Categories'


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    author = models.ForeignKey(Journalist, on_delete=models.SET_NULL, null=True, related_name='articles')
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news_articles'
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
        ordering = ['-published_date']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.article.title[:30]}"

    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-timestamp']


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    plan_type = models.CharField(max_length=50, choices=PLAN_CHOICES, default='free')

    def __str__(self):
        return f"{self.user.name} - {self.plan_type}"

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class Advertisement(models.Model):
    advertiser_name = models.CharField(max_length=100)
    content = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='advertisements')
    article = models.ForeignKey(NewsArticle, on_delete=models.SET_NULL, null=True, blank=True, related_name='advertisements')

    def __str__(self):
        return self.advertiser_name

    class Meta:
        db_table = 'advertisements'
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'