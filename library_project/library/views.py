from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from .models import Book, Loan, Author, Loan 
from .forms import BookForm, AuthorForm  


# ---------------- BOOKS ----------------
@login_required
def book_list(request):
    books = Book.objects.all()
    year = request.GET.get("year")

    if year:
        books = books.filter(year=year)

    genre = request.GET.get("genre")
    author = request.GET.get("author")
    available = request.GET.get("available")

    if genre:
        books = books.filter(genre__icontains=genre)

    if author:
        books = books.filter(authors__last_name__icontains=author)

    if available == "1":
        books = books.filter(available_copies__gt=0)

    return render(request, 'library/book_list.html', {'books': books})
  


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})


@login_required
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_detail', pk=pk)
    return render(request, 'library/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})


# ---------------- LOANS ----------------

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.available_copies > 0:
        Loan.objects.create(
            user=request.user,
            book=book,
            due_date=timezone.now().date() + timedelta(days=14)
        )

        book.available_copies -= 1
        book.save()

    return redirect('book_detail', pk=pk)


@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if loan.user == request.user and not loan.returned_at:
        loan.returned_at = timezone.now()
        loan.save()

        book = loan.book
        book.available_copies += 1
        book.save()

    return redirect('my_loans')


# ---------------- HISTORY ----------------

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, 'library/my_loans.html', {'loans': loans})



#-----------Autori--------------------
def author_list(request):
    authors = Author.objects.all()
    return render(request, "authors/author_list.html", {"authors": authors})


def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "authors/author_form.html", {"form": form})


def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
        return redirect("author_list")
    return render(request, "authors/author_form.html", {"form": form})


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect("author_list")
    return render(request, "authors/author_confirm_delete.html", {"author": author})


#----------------------Loan-----------------------


@login_required
def loan_list(request):
    if request.user.is_staff:
        loans = Loan.objects.all()
    else:
        loans = Loan.objects.filter(user=request.user)

    return render(request, "loans/loan_list.html", {"loans": loans})


@login_required
def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if request.user.is_staff:  # len admin môže mazať
        loan.delete()

    return redirect("loan_list")
