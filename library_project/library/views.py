from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .models import Book, Loan, Author, AdminActivity
from .forms import BookForm, AuthorForm, RegisterForm, ProfileEditForm, AdminUserEditForm


def is_admin(user):
    return user.is_staff


def log_activity(user, action):
    if user and user.is_authenticated:
        username = getattr(user, 'username', '') or 'deleted account'
        AdminActivity.objects.create(admin_user=user if getattr(user, 'pk', None) else None, account_name=username, account_type='admin' if user.is_staff else 'user', action=action)


def log_admin_activity(user, action):
    log_activity(user, action)


def common_filters_context():
    years = Book.objects.order_by('year').values_list('year', flat=True).distinct()
    oldest_year = years.first() if years else None
    return {"genres": [g[0] for g in Book.GENRE_CHOICES], "years": years, "oldest_year": oldest_year}


@login_required
def book_list(request):
    books = Book.objects.all().prefetch_related('authors')
    year = (request.GET.get("year") or "").strip()
    genre = (request.GET.get("genre") or "").strip()
    author = (request.GET.get("author") or "").strip()
    title = (request.GET.get("title") or "").strip()
    popular = request.GET.get("popular")

    if year and year.isdigit():
        oldest_year = Book.objects.order_by('year').values_list('year', flat=True).first()
        if oldest_year is None or int(year) >= int(oldest_year):
            books = books.filter(year=int(year))
    if genre:
        books = books.filter(genre__iexact=genre)
    if author:
        books = books.filter(Q(authors__first_name__icontains=author) | Q(authors__last_name__icontains=author)).distinct()
    if title:
        books = books.filter(title__icontains=title)
    if popular == "1":
        books = books.annotate(loan_count=Count('loan')).order_by('-loan_count', 'title')
    else:
        books = books.order_by('title')

    active_book_ids = []
    if request.user.is_authenticated:
        active_book_ids = list(Loan.objects.filter(user=request.user, returned_at__isnull=True).values_list('book_id', flat=True))
    context = {'books': books, 'selected_genre': genre, 'selected_year': year, 'author_query': author, 'title_query': title, 'active_book_ids': active_book_ids}
    context.update(common_filters_context())
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    has_active_loan = request.user.is_authenticated and Loan.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists()
    return render(request, 'library/book_detail.html', {'book': book, 'has_active_loan': has_active_loan})


@login_required
@user_passes_test(is_admin)
def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        book = form.save()
        log_admin_activity(request.user, f"Added book: {book.title}")
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        book = form.save()
        log_admin_activity(request.user, f"Edited book: {book.title}")
        return redirect('book_detail', pk=pk)
    return render(request, 'library/book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        log_admin_activity(request.user, f"Deleted book: {title}")
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    already_borrowed = Loan.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists()
    if not request.user.is_staff and book.computed_available_copies > 0 and not already_borrowed:
        Loan.objects.create(user=request.user, book=book, due_date=timezone.now().date() + timedelta(days=14))
        log_activity(request.user, f'Borrowed book: {book.title}')
    return redirect('book_detail', pk=pk)


@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if loan.user == request.user and not loan.returned_at:
        loan.returned_at = timezone.now().date()
        loan.save()
        log_activity(request.user, f'Returned book: {loan.book.title}')
    return redirect('my_loans')


@login_required
def my_loans(request):
    status = request.GET.get('status', 'borrowed')
    loans = Loan.objects.filter(user=request.user).select_related('book')
    if status == 'returned':
        loans = loans.filter(returned_at__isnull=False)
    else:
        loans = loans.filter(returned_at__isnull=True)
        status = 'borrowed'
    return render(request, 'library/my_loans.html', {'loans': loans, 'status': status})


@login_required
def profile(request):
    return render(request, 'library/profile.html')


@login_required
def profile_edit(request):
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        log_activity(request.user, 'Edited profile')
        return redirect('profile')
    return render(request, 'library/profile_edit.html', {'form': form, 'submitted': request.method == 'POST'})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        log_activity(user, 'Created account')
        return redirect('book_list')
    return render(request, 'library/register.html', {'form': form})


@login_required
def author_list(request):
    q = (request.GET.get('q') or '').strip()
    authors = Author.objects.annotate(borrow_count=Count('book__loan'))
    if q:
        authors = authors.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
    authors = authors.order_by('last_name', 'first_name')
    return render(request, "authors/author_list.html", {"authors": authors, "q": q})


@login_required
def author_detail(request, pk):
    author = get_object_or_404(Author.objects.prefetch_related('book_set'), pk=pk)
    return render(request, "authors/author_detail.html", {"author": author})


@login_required
@user_passes_test(is_admin)
def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        author = form.save()
        log_admin_activity(request.user, f"Added author: {author}")
        return redirect("author_list")
    return render(request, "authors/author_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        author = form.save()
        log_admin_activity(request.user, f"Edited author: {author}")
        return redirect("author_list")
    return render(request, "authors/author_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        name = str(author)
        author.delete()
        log_admin_activity(request.user, f"Deleted author: {name}")
        return redirect("author_list")
    return render(request, "authors/author_confirm_delete.html", {"author": author})


@login_required
def loan_list(request):
    loans = Loan.objects.all().select_related('book', 'user') if request.user.is_staff else Loan.objects.filter(user=request.user).select_related('book', 'user')
    return render(request, "loans/loan_list.html", {"loans": loans})


@login_required
def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.user.is_staff:
        info = f"{loan.book.title} / {loan.user.username}"
        loan.delete()
        log_admin_activity(request.user, f"Deleted loan: {info}")
    return redirect("loan_list")


@login_required
@user_passes_test(is_admin)
def admin_accounts(request):
    role = (request.GET.get('role') or '').strip()
    email = (request.GET.get('email') or '').strip()
    name = (request.GET.get('name') or '').strip()

    users = User.objects.all().order_by('username')

    if role == 'admin':
        users = users.filter(is_staff=True)
    elif role == 'user':
        users = users.filter(is_staff=False)

    if email:
        users = users.filter(email__icontains=email)

    if name:
        users = users.filter(
            Q(username__icontains=name) |
            Q(first_name__icontains=name) |
            Q(last_name__icontains=name)
        )

    return render(request, 'admin_tools/accounts.html', {
        'accounts': users,
        'selected_role': role,
        'email_query': email,
        'name_query': name,
    })


@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, pk):
    account = get_object_or_404(User, pk=pk)
    form = AdminUserEditForm(request.POST or None, instance=account)
    if request.method == 'POST' and form.is_valid():
        old_active = account.is_active
        old_staff = account.is_staff
        account = form.save()
        if old_active and not account.is_active:
            action_text = f"Suspended user account: {account.username}"
        elif not old_active and account.is_active:
            action_text = f"Restored user account: {account.username}"
        elif old_staff != account.is_staff:
            action_text = f"Changed account type: {account.username}"
        else:
            action_text = f"Edited user account: {account.username}"
        log_admin_activity(request.user, action_text)
        return redirect('admin_accounts')
    return render(request, 'admin_tools/account_form.html', {'form': form, 'account': account})


@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, pk):
    account = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = account.username
        # Log the activity before deleting the account. If an admin deletes their own account,
        # Django can set request.user.pk to None, which previously caused IntegrityError.
        log_admin_activity(request.user, f"Deleted user account: {username}")
        account.delete()
        return redirect('admin_accounts')
    return render(request, 'admin_tools/account_confirm_delete.html', {'account': account})


@login_required
@user_passes_test(is_admin)
def admin_activity(request):
    day = request.GET.get('day', '')
    time_value = request.GET.get('time', '')
    action = request.GET.get('action', '')
    account_type = request.GET.get('account_type', '')
    activities = AdminActivity.objects.select_related('admin_user').all()

    if day:
        activities = activities.filter(created_at__date=day)
    if time_value and len(time_value) >= 5:
        try:
            activities = activities.filter(created_at__hour=int(time_value[:2]), created_at__minute=int(time_value[3:5]))
        except ValueError:
            time_value = ''
    if action:
        activities = activities.filter(action=action)
    if account_type in ['admin', 'user']:
        activities = activities.filter(account_type=account_type)

    actions = AdminActivity.objects.order_by('action').values_list('action', flat=True).distinct()
    return render(request, 'admin_tools/activity.html', {
        'activities': activities,
        'day': day,
        'time_value': time_value,
        'selected_action': action,
        'selected_account_type': account_type,
        'actions': actions,
    })


@login_required
@user_passes_test(is_admin)
def admin_activity_undo(request, pk):
    activity = get_object_or_404(AdminActivity, pk=pk)
    action = activity.action or ''
    actor_name = activity.account_name or (activity.admin_user.username if activity.admin_user else '')

    if request.method != 'POST':
        return redirect('admin_activity')

    undone = False
    message = ''

    # Accounts
    if 'Suspended user account:' in action or ('Pozastavil' in action and 'používateľský účet:' in action):
        username = action.split(':', 1)[1].strip()
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            user_obj.is_active = True
            user_obj.save()
            undone = True
            message = f'Account {username} was activated again.'
    elif 'Restored user account:' in action or 'Obnovil používateľský účet:' in action:
        username = action.split(':', 1)[1].strip()
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            user_obj.is_active = False
            user_obj.save()
            undone = True
            message = f'Account {username} was marked as suspended again.'

    # User loans
    elif 'Borrowed book:' in action or 'Požičal knihu:' in action:
        title = action.split(':', 1)[1].strip()
        book = Book.objects.filter(title=title).first()
        user_obj = User.objects.filter(username=actor_name).first()
        if book and user_obj:
            loan = Loan.objects.filter(user=user_obj, book=book, returned_at__isnull=True).order_by('-borrowed_at', '-id').first()
            if loan:
                loan.delete()
                undone = True
                message = f'Loan for book {title} was canceled.'
    elif 'Returned book:' in action or 'Vrátil knihu:' in action:
        title = action.split(':', 1)[1].strip()
        book = Book.objects.filter(title=title).first()
        user_obj = User.objects.filter(username=actor_name).first()
        if book and user_obj:
            loan = Loan.objects.filter(user=user_obj, book=book, returned_at__isnull=False).order_by('-returned_at', '-id').first()
            if loan:
                loan.returned_at = None
                loan.save()
                undone = True
                message = f'Book {title} was marked as borrowed again.'

    # Added records can be removed when undoing the action.
    elif 'Added book:' in action or 'Pridal knihu:' in action:
        title = action.split(':', 1)[1].strip()
        book = Book.objects.filter(title=title).first()
        if book:
            book.delete()
            undone = True
            message = f'Added book {title} was removed.'
    elif 'Added author:' in action or 'Pridal autora:' in action:
        name = action.split(':', 1)[1].strip()
        parts = name.split()
        author = None
        if len(parts) >= 2:
            author = Author.objects.filter(first_name=parts[0], last_name=' '.join(parts[1:])).first()
        if author:
            author.delete()
            undone = True
            message = f'Added author {name} was removed.'

    if undone:
        activity.delete()
        log_admin_activity(request.user, f'Undid activity: {action}')
        messages.success(request, message or 'Activity was undone.')
    else:
        messages.warning(request, 'This activity cannot be undone automatically because the original data is missing or the record no longer exists.')

    return redirect('admin_activity')


class LibraryLoginView(LoginView):
    template_name = 'library/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Logged in')
        return response


@login_required
def logout_view(request):
    log_activity(request.user, 'Logged out')
    logout(request)
    return redirect('book_list')


def set_language(request, lang):
    if lang in ["sk", "en"]:
        request.session["lang"] = lang
    return redirect(request.META.get("HTTP_REFERER", "book_list"))


def set_theme(request, theme):
    if theme in ["light", "dark"]:
        request.session["theme"] = theme
    return redirect(request.META.get("HTTP_REFERER", "profile"))
