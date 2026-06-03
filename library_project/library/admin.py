from django.contrib import admin
from .models import Book, Author, Loan, AdminActivity


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'country', 'birth_date')
    search_fields = ('first_name', 'last_name', 'country')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'total_copies')
    search_fields = ('title', 'isbn', 'authors__first_name', 'authors__last_name')
    list_filter = ('genre', 'year')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'returned_at')
    readonly_fields = ('user', 'book', 'borrowed_at', 'due_date', 'returned_at')

    def has_add_permission(self, request):
        return False


@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'admin_user', 'action')
    list_filter = ('created_at', 'admin_user')
    search_fields = ('admin_user__username', 'action')
    readonly_fields = ('admin_user', 'action', 'created_at')

    def has_add_permission(self, request):
        return False
