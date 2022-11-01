from django.contrib import admin

from .models import User, Book, Watchlist, BookSellers, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookSellers)
admin.site.register(Watchlist)
admin.site.register(Message)

