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

    # Custom Admin Panel
    path('my-admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('my-admin/articles/', views.admin_articles, name='admin_articles'),
    path('my-admin/articles/<int:pk>/delete/', views.admin_article_delete, name='admin_article_delete'),
    path('my-admin/users/', views.admin_users, name='admin_users'),
    path('my-admin/users/<int:pk>/toggle-staff/', views.admin_user_toggle_staff, name='admin_user_toggle_staff'),
    path('my-admin/comments/', views.admin_comments, name='admin_comments'),
    path('my-admin/comments/<int:pk>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
    path('my-admin/categories/', views.admin_categories, name='admin_categories'),
    path('my-admin/subscriptions/', views.admin_subscriptions, name='admin_subscriptions'),
]