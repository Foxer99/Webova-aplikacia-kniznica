from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),

    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('loan/<int:loan_id>/return/', views.return_book, name='return_book'),

    path('my-loans/', views.my_loans, name='my_loans'),
]