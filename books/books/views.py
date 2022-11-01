import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.db.models import Q
import urllib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.db.models import Count

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token

from .forms import RegisterForm, LoginForm, UpdateAccountForm, SellBookForm, ContactUsForm, RateUserForm
from .models import User, Book, Watchlist, Ratings, BookSellers, Message
from .filters import BookFilter, BookFilterWatchlist

CATEGORIES_SET = (
    'Art',
    'Antiques & Collectibles',  
    'Architecture',
    'Psychology',
    'Philosophy',
    'Adventure',
    'Romance',
    'Biography & Autobiography',
    'Body, Mind & Spirit',      
    'Business & Economics',     
    'Computers',
    'Crafts & Hobbies',
    'Design',
    'Drama',
    'Education',
    'Foreign Language Study',   
    'Gardening',
    'House & Home',
    'Language Arts & Disciplines',
    'Law',
    'Mathematic',
    'Pets',
    'Photography',
    'Religion',
    'Science',
    'Fiction',
    'Non-Fiction',
    'Travel',
    'True Crime',
    'Games & Activities',
    'Humor',
    'Juvenile Fiction',
    'Juvenile Nonfiction',
    'Medical',
    'Cooking',
    'Self-help',
    'Music',
    'Health & Fitness',
    'History',
    'Nature',
    'Performing Arts',
    'Poetry',
    'Family & Relationships',
    'Political Science',
    'Social Science',
    'Sports & Recreation',
    'Technology',
    'Unknown',
)

CATEGORIES_SET_SLUG = (
    'art',
    'antiques-collectibles',
    'architecture',
    'psychology',
    'philosophy',
    'adventure',
    'romance',
    'biography-autobiography',
    'body-mind-spirit',
    'business-economics',
    'computers',
    'crafts-hobbies',
    'design',
    'drama',
    'education',
    'foreign-language-study',
    'gardening',
    'house-home',
    'language-arts-disciplines',
    'law',
    'mathematic',
    'pets',
    'photography',
    'religion',
    'science',
    'fiction',
    'non-fiction',
    'travel',
    'true-crime',
    'games-activities',
    'humor',
    'juvenile-fiction',
    'juvenile-nonfiction',
    'medical',
    'cooking',
    'self-help',
    'music',
    'health-fitness',
    'history',
    'nature',
    'performing-arts',
    'poetry',
    'family-relationships',
    'political-science',
    'social-science',
    'sports-recreation',
    'technology',
    'unknown',
)

# Create your views here.
def index(request):
 
    return render(request, 'index.html', {
        'books_offers': BookSellers.objects.filter(is_sold=False).order_by('-date_added')[:12],
        'books_requests': Watchlist.objects.all().order_by('-date_added')[:12],
        'top_sellers': User.objects.annotate(offers=Count('booksellers__book')).order_by('-offers')[:5],
    })
    # return render(request, 'index1.html')

# Handle Categories
def categories(request):

    return render(request, 'categories/categories.html', {
        'categories': CATEGORIES_SET,
    })

def category(request, category_name):

    if category_name not in CATEGORIES_SET_SLUG:
        raise Http404


    books_in_category = Book.objects.filter(category=category_name).order_by('-date_added')
    paginator = Paginator(books_in_category, 8)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''


    return render(request, 'categories/category.html', {
        'category': category_name.title().replace('-', ' '),
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'total_count': Book.objects.filter(category=category_name).count()
    })

# Handle How it works
def how_it_works(request):
    return render(request, 'how_it_works.html', {})

# Handle Books
def books(request):
    
    books = Book.objects.all().order_by('-date_added')
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)


    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = f''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    return render(request, 'books/books.html', {
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'books_total_count': Book.objects.count(),
    })

# Handle Books Offers
def books_offers(request):

    
    books = BookFilter(
        request.GET,
        queryset = BookSellers.objects.filter(is_sold=False).order_by('-date_added')
    )

    paginator = Paginator(books.qs, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'books/books_offers.html', {
        'filter': books,
        'page': page,
        'books_total_count': BookSellers.objects.filter(is_sold=False).count(),
    })

# Handle Books Requests
def books_requests(request):


    books = BookFilterWatchlist(
        request.GET,
        queryset = Watchlist.objects.all().order_by('date_added')
    )

    paginator = Paginator(books.qs, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'books/books_requests.html', {
        'filter': books,
        'page': page,
        'books_total_count': Watchlist.objects.all().count(),
    })

def book_view(request, book_id, book_title):

    book = Book.objects.get(id=book_id)

    if request.user.is_authenticated and request.method == 'POST' and 'insert_into_watchlist' in request.POST:
        if Watchlist.objects.filter(user=request.user, book=book).exists():
            remove_from_watchlist = Watchlist.objects.get(user=request.user, book=book)
            remove_from_watchlist.delete()
            messages.success(request, 'Book removed from your watchlist.')
        else:
            book_watchlisted = Watchlist.objects.create(user=User.objects.get(id=request.user.id), book=book)
            book_watchlisted.save()
            messages.success(request, 'We will notify you should someone offer this book :)')
    elif request.method == 'POST' and 'sold_to' in request.POST and Watchlist.objects.filter(book=book_id) is not None:
        book_sold = BookSellers.objects.get(book=book, user=request.user, is_sold=False)
        buyer_id = request.POST["sold_to_user"]
        book_sold.sold_to = User.objects.get(id=buyer_id)
        book_sold.is_sold = True
        book_sold.save()
        messages.success(request, 'Great, you sold your copy of the book.')
    elif request.user.is_authenticated and request.method == 'POST' and 'delete_my_offer' in request.POST:
        to_remove = BookSellers.objects.get(book=book, user=request.user)
        to_remove.delete()
        messages.success(request, 'Your offer was successfully deleted.')

    return render(request, 'books/book.html', {
        'book': book,
        'book_offers': BookSellers.objects.filter(book=book),
        'is_offered': True if BookSellers.objects.filter(book=book, is_sold=False).exists() else False,
        'sellers_count': BookSellers.objects.filter(book=book, is_sold=False).count(),
        'sellers': BookSellers.objects.filter(book=book, is_sold=False),
        'watchlist': Watchlist.objects.filter(book=book),
        'already_on_watchlist': True if request.user.is_authenticated and Watchlist.objects.filter(user_id=request.user.id, book=book) else False,
        'is_seller': True if request.user.is_authenticated and BookSellers.objects.filter(book=book, user=request.user, is_sold=False).exists() else False,
        'buyers': Watchlist.objects.filter(book=book),
        'already_rated': True if request.user.is_authenticated and Ratings.objects.filter(book=book, user_rating=request.user).exists() else False,
        'rating_id': Ratings.objects.get(book=book, user_rating=request.user).id if request.user.is_authenticated and Ratings.objects.filter(book=book, user_rating=request.user).exists() else None,
        'full_url': request.build_absolute_uri(),
        })

@login_required
def book_sell(request):

    form = SellBookForm()

    if request.method == 'POST':
        form = SellBookForm(request.POST)

        pages = request.POST['pages']
        date_published = request.POST['date_published']
        description = request.POST['description']
        identifier = request.POST['identifier']
        price = request.POST['price']
        condition = request.POST['condition']
        add_info = request.POST['add_info']
        is_selling = request.POST['is_selling']
       
        # Price included, must be a selling offer
        if is_selling == 'true' and price and form.is_valid():

            if int(price) >= 0:
                new_book = form.save(commit=False)
                new_book.published_year = date_published
                new_book.page_count = pages
                new_book.description = description
                new_book.identifier = identifier
                new_book.save()
                
                if request.POST['cover_img']:
                    with open(f'/home/peterhrncirik/mysite/media/{new_book.id}.jpg', 'wb') as cover:
                        cover.write(urllib.request.urlopen(request.POST['cover_img']).read())

                    new_book.cover = f'{new_book.id}.jpg'
                    new_book.save()
            
                new_seller = BookSellers.objects.create(book=new_book, user=request.user, price=price, condition=condition, additional_info=add_info)
                new_seller.save()

                messages.success(request, 'Book successfully listed for sale.')
                return redirect('user_account', username=request.user)
            else:
                messages.warning(request, 'Please include correct price.')
        # price excluded, must be watchlist request    
        elif form.is_valid():

            form = SellBookForm(request.POST)

            new_book = form.save(commit=False)
            new_book.published_year = date_published
            new_book.page_count = pages
            new_book.description = description
            new_book.identifier = identifier
            new_book.save()
            
            if request.POST['cover_img']:
                with open(f'/home/peterhrncirik/mysite/media/{new_book.id}.jpg', 'wb') as cover:
                    cover.write(urllib.request.urlopen(request.POST['cover_img']).read())

                new_book.cover = f'{new_book.id}.jpg'
                new_book.save()
            
            new_request = Watchlist.objects.create(book=new_book, user=request.user)
            new_request.save()

            messages.success(request, 'You have successfully listed a book.')
            return redirect('user_account', username=request.user)
        else:
            messages.warning(request, 'Please mention all required information.')

    return render(request, 'books/book_sell.html', {'form': form})

@login_required
def book_quick_sell(request, book_id, title):

    book = Book.objects.get(id=book_id)

    if request.method == 'POST':

        if BookSellers.objects.filter(book=book, user=request.user).exists():
            user_offers = BookSellers.objects.filter(book=book, user=request.user)
            for offer in user_offers:
                if not offer.is_sold:
                    messages.warning(request, 'Looks like you are already offering this book.')
                    return redirect('book', book_id=book.id, book_title=book.slug)

        price = request.POST['price']
        condition = request.POST['condition']
        add_info = request.POST['add_info']

        if not price:
            price = 0
        
        new_listing = BookSellers.objects.create(book=book, user=request.user, price=price, condition=condition, additional_info=add_info) 
        new_listing.save()

        messages.success(request, 'Book successfully listed for sale.')
        return redirect('user_account', username=request.user)


    return render(request, 'books/book_quick_sell.html', {
        'book': book,
    })

@login_required
@api_view(['GET'])
def find_book(request):

    param = request.GET.get('param')
    b_id = request.GET.get('bid')

    if b_id:
        book = Book.objects.get(identifier=b_id)
        if book is not None:
            return Response({
                'found': True,
                'id': book.id,
                'title': book.slug,
            }, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
    if param:
        url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{param}&fields=items(id,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers,volumeInfo/description)&key=AIzaSyDjrM5K4xzt7p601ROtsFAY7ZftORmBnsQ'
        r = requests.get(url)
        
        if r.status_code == 200:
            data = r.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Request failed"}, status=r.status_code)
    else:
        return Response({}, status=status.HTTP_200_OK)

@login_required
def book_update(request, book_id, book_title):

    # Make sure logged-in user is actual author
    if not Book.objects.filter(id=book_id, user=request.user):
        return redirect('index')

    form = SellBookForm(request.POST or None, instance=Book.objects.get(id=book_id))
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated information for this book.')
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('user_account', name=request.user)

    return render(request, 'books/book_update.html', {'form': form, 'book_id': book_id, 'book_title': book_title})

# Handle Search
def search(request):

    search_query = request.GET.get('query', '')
    if search_query:
        results = Book.objects.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query) | Q(ISBN__icontains=search_query) | Q(description__icontains=search_query))
        results_count = results.count()
        # bug here, search pagination throws error, template pagination is hidden and amount of results is higher
        paginator = Paginator(results, 50)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        if page.has_next():
            next_url = f'?page={page.next_page_number()}'
        else:
            next_url = f''

        if page.has_previous():
            prev_url = f'?page={page.previous_page_number()}'
        else:
            prev_url = ''

        return render(request, 'search/search_results.html', {
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'results_count': results_count,
        'search_term': request.GET.get('query'),
        })
    # else:
        # books = Book.objects.all()
        # results_count = Book.objects.filter(title__icontains=search_query).count()

    return render(request, 'search/search.html', {})

# Live search
@api_view(['GET'])
def live_search(request):

    query = request.GET.get('query')

    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(ISBN__icontains=query)).values('id', 'title', 'cover', 'author', 'slug')
        if books:
            return Response(books, status=status.HTTP_200_OK)
        else:
            return Response({'e': "We couldn't find this book, try searching for something else instead."}, status=status.HTTP_200_OK)

# Handle user account
def user_account(request, username):

    # Query the user
    current_user = User.objects.get(username=username)

    user_books = BookSellers.objects.filter(user=current_user, is_sold=False).order_by('-date_added')
    paginator = Paginator(user_books, 8)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = f''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    return render(request, 'user/user_account.html', {
        'current_user': current_user,
        'offers_count': BookSellers.objects.filter(user=current_user, is_sold=False).count(),
        'request_count': Watchlist.objects.filter(user=current_user).count(),
        'is_actual_user': current_user == request.user,
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'has_any_contact_info': True if current_user.district or current_user.mobile or current_user.first_name or current_user.last_name else False,
        })

def user_account_requests(request, username):
    
    # Query the user
    current_user = User.objects.get(username=username)

    user_books = Watchlist.objects.filter(user=current_user).order_by('-date_added')
    paginator = Paginator(user_books, 8)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = f''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    return render(request, 'user/user_account_requests.html', {
        'current_user': current_user,
        'offers_count': BookSellers.objects.filter(user=current_user, is_sold=False).count(),
        'request_count': Watchlist.objects.filter(user=current_user).count(),
        'is_actual_user': current_user == request.user,
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
        'has_any_contact_info': True if current_user.district or current_user.mobile or current_user.first_name or current_user.last_name else False,
        })

@login_required
def user_account_update(request, username):

    # Make sure logged-in user is accessing his own update page
    current_user = get_object_or_404(User, id=User.objects.get(username=username).id)
    if current_user != request.user:
        return redirect('user_account', username = request.user)

    form = UpdateAccountForm(request.POST or None, instance=current_user)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, 'Account information successfully updated.')
            return redirect('user_account', username=request.POST['username'])
        



    return render(request, 'user/user_account_update.html', {
        'form': form,
        'current_user': current_user
        })

@login_required
def user_rate(request, username, book_id):

    # Make sure logged-in user is actual buyer and can rate the seller
    if not BookSellers.objects.filter(book_id=book_id, sold_to=request.user).exists():
        return redirect('index')

    form = RateUserForm()
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = RateUserForm(request.POST)

        if form.is_valid() and not Ratings.objects.filter(book=book, user_rating=request.user).exists():
            new_rating = form.save(commit=False)
            new_rating.user_rated = User.objects.get(username=username)
            new_rating.user_rating = request.user
            new_rating.book = Book.objects.get(id=book_id)

            if request.POST['rating'] == 'good':
                user_rated = User.objects.get(username=username)
                user_rated.rating_good += 1
                user_rated.save()
            elif request.POST['rating'] == 'medium':
                user_rated = User.objects.get(username=username)
                user_rated.rating_medium += 1
                user_rated.save()
            elif request.POST['rating'] == 'bad':
                user_rated = User.objects.get(username=username)
                user_rated.rating_bad += 1
                user_rated.save()

            new_rating.save()

            messages.success(request, 'You have successfully rated the seller')
            return redirect('book', book.id, book.title)
        else:
            messages.warning(request, 'You have already rated the seller of this book.')
            return redirect('user_account', request.user)

    return render(request, 'user/user_rate.html', {
        'username': username,
        'book': book,
        'form': form,
    })

def user_ratings(request, username):

    ratings = Ratings.objects.filter(user_rated=User.objects.get(username=username))
    return render(request, 'user/user_ratings.html', {
        'username': username,
        'ratings': ratings,
    })

def user_rating(request, username, rating_id):
    return render(request, 'user/user_rating.html', {
        'rating': Ratings.objects.get(id=rating_id),
        'username': username,
    })

@login_required
def contact_user(request, username):    

    if request.method == 'POST':

        try:
            message = request.POST['message']
            
            if message:
                receiver = User.objects.get(username=username)
                send_mail(
                    'Someone sent you a new message on Books',
                    f'\n Hey, {username.title()}! \n\n You have a new message from {request.user.username.title()} received. \n\n It says: {message}. \n\n You can contact the person on their E-Mail: {request.user.email}. \n\n Please don\'t answer on this E-Mail. \n\n You can reach us at info@books.com. \n\n Happy reading!',
                    'info@books.com',
                    [receiver.email],
                    fail_silently=True,
                )

                messages.success(request, 'Notification sent.')
                return redirect('user_account', username = request.user)
            else:
                messages.warning(request, 'You forgot to mention actual message :)')
        except:
            messages.error(request, 'Something happened. Please try again later.')
        

    return render(request, 'contact/contact_user.html', {
        'receiver': username,
        })

@login_required
def contact_user_book(request, username, book_id, offer_id):    

    book = Book.objects.get(id=book_id)

    if request.method == 'POST':

        try:
            message = request.POST['message']
            
            if message:
                receiver = User.objects.get(username=username)
                send_mail(
                    'Someone sent you a new message on Books',
                    f'\n Hey, {username.title()}! \n\n You have a new message from {request.user.username.title()} received. \n\n It says: {message}. \n\n You can contact the person on their E-Mail: {request.user.email}. \n\n Please don\'t answer on this E-Mail. \n\n You can reach us at info@books.com. \n\n Happy reading!',
                    'info@books.com',
                    [receiver.email],
                    fail_silently=True,
                )

                messages.success(request, 'Notification sent.')
                return redirect('user_account', username = request.user)
            else:
                messages.warning(request, 'You forgot to mention actual message :)')
        except:
            messages.error(request, 'Something happened. Please try again later.')
        

    return render(request, 'contact/contact_user_book.html', {
        'book': book,
        'receiver': username,
        'condition': BookSellers.objects.get(id=offer_id, book=book, user=User.objects.get(username=username)).condition,
        'additional_info': BookSellers.objects.get(id=offer_id, book=book, user=User.objects.get(username=username)).additional_info,
        })

# User messages
@login_required
def user_messages(request, username):

    user = User.objects.get(username=username)
    messages = Message.objects.filter(sender=user)

    return render(request, 'user/user_messages.html', {'messages': messages})

# User messages
@login_required
def user_messages_chat(request, username, receiver_id):

    # receiver = User.objects.get(id=receiver_id)
    user = User.objects.get(username=username)
    messages = Message.objects.filter(sender_id=user.id, receiver_id=receiver_id)
    print(messages)

    return render(request, 'user/user_messages_chat.html', {'messages': messages})

# Handle contact us
def contact_us(request):

    if request.method == 'POST':

        try:
            message = request.POST['message']
            sender = request.POST['email']
            name = request.POST['name']
            
            if message and sender:
                
                send_mail(
                    'Message from contact form',
                    f'Name: {name.title()}. \n\n Email: {sender} \n\n Message: {message} \n\n',
                    'info@wienbuecher.at',
                    ['info@wienbuecher.at'],
                    fail_silently=True,
                )

                messages.success(request, 'Thanks for the message, we will get back to you :)')
            else:
                messages.warning(request, 'Please give us your E-Mail as well as message :)')
        except:
            messages.error(request, 'Contact form is currently disabled.')
            # messages.error(request, 'Something happend, please try again later.')

    return render(request, 'contact/contact_us.html', {})

# Handle user authenticaion
def registerPage(request):

    # If the user is logged-in, send him back to index page
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
  
            current_site = get_current_site(request)
            email_subject = 'Activate your Books account'
            message = render_to_string('auth/activate_plain.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.id)),
                'token': generate_token.make_token(new_user), 
            })

            text_message = strip_tags(message)

            email = EmailMultiAlternatives(
                'Activate your Books account', text_message, 'info@books.com', [new_user.email]
            )
            email.attach_alternative(message, 'text/html')
            
            # email = EmailMessage(
            #     email_subject,
            #     message,
            #     'no-reply@vienna-books.com',
            #     [new_user.email],
            # )

            email.send()

            messages.success(request, 'Registration successful. Please activate your account. We have sent you a link on your E-Mail address.')
            return redirect('login')
    
    return render(request, 'user/register.html', {'form': form})

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except Exception as identifier:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Account activated. You may now login.')
        return redirect('login')
    else:
        messages.error(request, 'Something went wrong.')
        return redirect('login')

# def welcome(request):

#     current_site = get_current_site(request)
#     email_subject = 'Welcome onboard!'
#     message = render_to_string('auth/welcome.html', {
#         'user': 'Peter',
#         'from': 'team@vienna-books.com'
#     })

#     email = EmailMessage(
#         email_subject,
#         message,
#         'noreply@vienna-books.com',
#         [new_user.email],
#     )

#     email.send()

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_verified:

            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
        elif user is not None and not user.is_verified:
            messages.warning(request, "Your account was not yet activated.")
        else:
            messages.error(request, 'Username or password is not correct.')

    return render(request, 'user/login.html', {'form': LoginForm()})

def logoutUser(request):

    logout(request)
    # messages.info(request, 'Successfully logged-out.')
    return redirect('index')

# Hadnle errors

def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'500.html', data)