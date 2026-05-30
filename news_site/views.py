from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import (
    NewsArticle, Category, Comment, User,
    Journalist, Advertisement, Subscription
)
from .forms import CommentForm, SubscribeForm, RegisterForm, ArticleForm, CategoryForm

def admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapped

def journalist_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Journalist', 'Admin']).exists()):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapped

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser or user.groups.filter(name='Admin').exists():
                return redirect('custom_admin_dashboard')
            return redirect('home')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    articles = NewsArticle.objects.select_related('category', 'author').all()[:12]
    categories = Category.objects.all()
    featured = NewsArticle.objects.order_by('-views').first()
    latest = NewsArticle.objects.order_by('-published_date')[:5]
    ads = Advertisement.objects.all()[:3]
    context = {
        'articles': articles,
        'categories': categories,
        'featured': featured,
        'latest': latest,
        'ads': ads,
    }
    return render(request, 'home.html', context)


def article_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    article.views += 1
    article.save()
    comments = article.comments.select_related('user').all()
    related = NewsArticle.objects.filter(category=article.category).exclude(pk=article.pk)[:4]
    ads = Advertisement.objects.filter(article=article)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            content = comment_form.cleaned_data['content']
            user, _ = User.objects.get_or_create(email=email, defaults={'name': name})
            Comment.objects.create(user=user, article=article, content=content)
            return redirect('article_detail', slug=article.slug)

    context = {
        'article': article,
        'comments': comments,
        'related': related,
        'comment_form': comment_form,
        'ads': ads,
    }
    return render(request, 'article_detail.html', context)


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = NewsArticle.objects.filter(category=category).select_related('author')
    categories = Category.objects.all()
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'category.html', context)


def journalist_detail(request, slug):
    journalist = get_object_or_404(Journalist, slug=slug)
    articles = NewsArticle.objects.filter(author=journalist).order_by('-published_date')
    context = {
        'journalist': journalist,
        'articles': articles,
    }
    return render(request, 'journalist.html', context)


def search(request):
    query = request.GET.get('q', '')
    articles = []
    if query:
        articles = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).select_related('category', 'author')
    context = {
        'articles': articles,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'search.html', context)


def subscribe(request):
    form = SubscribeForm()
    success = False
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            plan = form.cleaned_data['plan_type']
            user, _ = User.objects.get_or_create(email=email, defaults={'name': name})
            Subscription.objects.create(user=user, plan_type=plan)
            success = True
    return render(request, 'subscribe.html', {'form': form, 'success': success})


@journalist_required
def article_create(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            journalist = getattr(request.user, 'journalist_profile', None)
            article = NewsArticle.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                category=form.cleaned_data['category'],
                image=form.cleaned_data.get('image'),
                created_by=request.user,
                author=journalist
            )
            return redirect('article_detail', slug=article.slug)
    return render(request, 'article_create.html', {'form': form})


@journalist_required
def article_edit(request, slug):
    # Allow admins to edit any article, journalists only their own
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        article = get_object_or_404(NewsArticle, slug=slug)
    else:
        article = get_object_or_404(NewsArticle, slug=slug, created_by=request.user)
    form = ArticleForm(initial={
        'title': article.title,
        'content': article.content,
        'category': article.category,
    })
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.category = form.cleaned_data['category']
            if form.cleaned_data.get('image'):
                article.image = form.cleaned_data['image']
            article.save()
            return redirect('article_detail', slug=article.slug)
    return render(request, 'article_create.html', {'form': form, 'edit': True})


@journalist_required
def article_delete(request, slug):
    # Allow admins to delete any article, journalists only their own
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        article = get_object_or_404(NewsArticle, slug=slug)
    else:
        article = get_object_or_404(NewsArticle, slug=slug, created_by=request.user)
    
    if request.method == 'POST':
        article.delete()
        return redirect('home')
    return render(request, 'article_delete.html', {'article': article})


@journalist_required
def my_articles(request):
    articles = NewsArticle.objects.filter(created_by=request.user).order_by('-published_date')
    return render(request, 'my_articles.html', {'articles': articles})

@admin_required
def custom_admin_dashboard(request):
    context = {
        'total_articles': NewsArticle.objects.count(),
        'total_users': AuthUser.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_subscriptions': Subscription.objects.count(),
        'total_journalists': Journalist.objects.count(),
        'total_categories': Category.objects.count(),
        'latest_articles': NewsArticle.objects.select_related('category', 'author').order_by('-published_date')[:5],
        'latest_comments': Comment.objects.select_related('user', 'article').order_by('-timestamp')[:5],
    }
    return render(request, 'custom_admin/dashboard.html', context)


@admin_required
def admin_articles(request):
    articles = NewsArticle.objects.select_related('category', 'author', 'created_by').order_by('-published_date')
    return render(request, 'custom_admin/articles.html', {'articles': articles})


@admin_required
def admin_article_delete(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('admin_articles')
    return render(request, 'custom_admin/confirm_delete.html', {
        'obj': article,
        'type': 'maqola',
        'back_url': 'admin_articles'
    })


@admin_required
def admin_users(request):
    users = AuthUser.objects.all().order_by('-date_joined')
    return render(request, 'custom_admin/users.html', {'users': users})


@admin_required
def admin_user_toggle_staff(request, pk):
    user = get_object_or_404(AuthUser, pk=pk)
    if request.method == 'POST' and not user.is_superuser:
        user.is_staff = not user.is_staff
        user.save()
    return redirect('admin_users')


@admin_required
def admin_comments(request):
    comments = Comment.objects.select_related('user', 'article').order_by('-timestamp')
    return render(request, 'custom_admin/comments.html', {'comments': comments})


@admin_required
def admin_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('admin_comments')
    return render(request, 'custom_admin/confirm_delete.html', {
        'obj': comment,
        'type': 'izoh',
        'back_url': 'admin_comments'
    })


@admin_required
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/categories.html', {'categories': categories})


@admin_required
def admin_subscriptions(request):
    subs = Subscription.objects.select_related('user').order_by('-start_date')
    return render(request, 'custom_admin/subscriptions.html', {'subs': subs})


@admin_required
def admin_category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    return render(request, 'custom_admin/category_form.html', {'form': form, 'title': 'Create category'})


@admin_required
def admin_category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    return render(request, 'custom_admin/category_form.html', {'form': form, 'title': 'Edit category', 'edit': True})


@admin_required
def admin_category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_categories')
    return render(request, 'custom_admin/confirm_delete.html', {
        'obj': category,
        'type': 'kategoriya',
        'back_url': 'admin_categories'
    })