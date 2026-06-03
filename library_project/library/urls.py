from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    # ---------------- BOOKS ----------------
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # ---------------- BORROW / RETURN ----------------
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('loan/<int:loan_id>/return/', views.return_book, name='return_book'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # ---------------- AUTHORS ----------------
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/<int:pk>/edit/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # ---------------- LOANS ----------------
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/<int:pk>/delete/', views.loan_delete, name='loan_delete'),

    # ---------------- ADMIN TOOLS ----------------
    path('admin-accounts/', views.admin_accounts, name='admin_accounts'),
    path('admin-accounts/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-accounts/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-activity/', views.admin_activity, name='admin_activity'),
    path('admin-activity/<int:pk>/undo/', views.admin_activity_undo, name='admin_activity_undo'),

    # ---------------- AUTH ----------------
    path('login/', views.LibraryLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
    path('set-theme/<str:theme>/', views.set_theme, name='set_theme'),
    path('logout/', views.logout_view, name='logout'),
]