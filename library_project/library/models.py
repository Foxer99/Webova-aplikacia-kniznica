from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField(default=0)

    # M:N vzťah
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
   
    def __str__(self):
        return f"{self.book} - {self.user}"