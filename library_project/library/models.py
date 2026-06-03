from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birth_date = models.DateField()
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    GENRE_CHOICES = [
        ("Romantika", "Romantika"),
        ("Fantasy", "Fantasy"),
        ("Sci-fi", "Sci-fi"),
        ("Detektívka", "Detektívka"),
        ("Thriller", "Thriller"),
        ("Biografie", "Biografie"),
        ("História", "História"),
        ("Pre deti", "Pre deti"),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    year = models.IntegerField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    total_copies = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    available_copies = models.IntegerField(default=0)  # Legacy field kept for database compatibility
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    authors = models.ManyToManyField(Author)

    @property
    def borrowed_count(self):
        return self.loan_set.filter(returned_at__isnull=True).count()

    @property
    def computed_available_copies(self):
        return max(self.total_copies - self.borrowed_count, 0)

    def __str__(self):
        return self.title


class AdminActivity(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    account_name = models.CharField(max_length=150, blank=True, default='')
    account_type = models.CharField(max_length=20, blank=True, default='')
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.account_name or (self.admin_user.username if self.admin_user else 'deleted account')
        return f'{username} - {self.action} - {self.created_at}'


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book} - {self.user}"
