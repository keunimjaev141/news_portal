from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.utils.text import slugify
import random
import string


class Journalist(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='journalist_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    email = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            if not base_slug:
                base_slug = 'journalist'
            slug = base_slug
            while Journalist.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{''.join(random.choices(string.digits, k=4))}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'journalists'
        verbose_name = 'Journalist'
        verbose_name_plural = 'Journalists'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            if not base_slug:
                base_slug = 'category'
            slug = base_slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{''.join(random.choices(string.digits, k=4))}"
            self.slug = slug
        super().save(*args, **kwargs)

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


class PortalCategory(models.Model):
    portal = models.ForeignKey(NewsPortal, on_delete=models.CASCADE, related_name='portal_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='portal_categories')

    class Meta:
        db_table = 'portal_categories'
        unique_together = ('portal', 'category')


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    author = models.ForeignKey(Journalist, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_articles')
    published_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = 'article'
            slug = base_slug
            while NewsArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{''.join(random.choices(string.digits, k=4))}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news_articles'
        ordering = ['-published_date']


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.article.title[:30]}"

    class Meta:
        db_table = 'comments'
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


class Advertisement(models.Model):
    advertiser_name = models.CharField(max_length=100)
    content = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, related_name='advertisements')
    article = models.ForeignKey(NewsArticle, on_delete=models.SET_NULL, null=True, blank=True, related_name='advertisements')

    def __str__(self):
        return self.advertiser_name

    class Meta:
        db_table = 'advertisements'