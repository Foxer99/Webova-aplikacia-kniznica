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

    # ---------------- AUTHORS ----------------
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # ---------------- LOANS ----------------
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/<int:pk>/delete/', views.loan_delete, name='loan_delete'),

    # ---------------- AUTH ----------------
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]