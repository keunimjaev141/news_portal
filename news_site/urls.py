from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('category/<int:pk>/', views.category_articles, name='category_articles'),
    path('journalist/<int:pk>/', views.journalist_detail, name='journalist_detail'),
    path('search/', views.search, name='search'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'), 
    path('my-articles/', views.my_articles, name='my_articles'), 
]
