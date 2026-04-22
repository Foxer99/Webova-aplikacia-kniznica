from django.contrib import admin
from .models import Book, Author, Loan

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Loan)