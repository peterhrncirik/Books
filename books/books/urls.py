from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap
}

urlpatterns = [
    path('', views.index, name='index'),

    # User authentication 
    path('login/', views.loginPage, name='login'),
    # path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # Verify account
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # User account
    path('user/<str:username>/', views.user_account, name='user_account'),
    path('user/<str:username>/requests/', views.user_account_requests, name='user_account_requests'),
    path('user/update/<str:username>/', views.user_account_update, name='user_account_update'),

    # Rate user
    path('user/<str:username>/book/<int:book_id>/rate/', views.user_rate, name='user_rate'),
    path('user/<str:username>/ratings/', views.user_ratings, name='user_ratings'),
    path('user/<str:username>/rating/<int:rating_id>/', views.user_rating, name='user_rating'),

    # Contact user general
    path('contact/<str:username>/', views.contact_user, name='contact_user'),

    # Contact user book
    path('contact/<str:username>/<int:book_id>/<int:offer_id>/', views.contact_user_book, name='contact_user_book'),

    # User messages
    path('user/<str:username>/messages/', views.user_messages, name='user_messages'),
    path('user/<str:username>/messages/<int:receiver_id>/', views.user_messages_chat, name='user_messages_chat'),

    # Contact us
    path('contact-us/', views.contact_us, name='contact_us'),

    # Books
    path('books/', views.books, name='books'),
    path('books/offers/', views.books_offers, name='books_offers'),
    path('books/requests/', views.books_requests, name='books_requests'),
    path('book/add/', views.book_sell, name='book_add'),
    path('book/<int:book_id>/<slug:book_title>/', views.book_view, name='book'),
    path('book/<int:book_id>/<str:book_title>/update/', views.book_update, name='book_update'),
    path('book/request/search/', views.find_book, name='find_book'),

    # Quick Sell
    path('book/quick-sell/<int:book_id>/<str:title>/', views.book_quick_sell, name='book_quick_sell'),

    # Category
    path('categories/', views.categories, name='categories'),
    path('category/<str:category_name>/', views.category, name='category'),

    # Search
    path('search/', views.search, name='search'),

    # Live Search,
    path('find/', views.live_search, name='live_search'),

    # How it works
    path('how-does-it-work/', views.how_it_works, name='how_it_works'),

    # Sitemap
    path('books/sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

# Handle errors
handler404 = 'books.views.error_404'
handler500 = 'books.views.error_500'