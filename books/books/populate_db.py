
import random

def generate_users():

    DISTRICTS = (
    ('1010, Innenstadt'),
    ('1020, Leopoldstadt'),
    ('1030, Landstraße'),
    ('1040, Wieden'),
    ('1050, Margareten'),
    ('1060, Mariahilf'),
    ('1070, Neubau'),
    ('1080, Josefstadt'),
    ('1090, Alsergrund'),
    ('1100, Favoriten'),
    ('1110, Simmering'),
    ('1120, Meidling'),
    ('1130, Hietzing'),
    ('1140, Penzing'),
    ('1150, Rudolfsheim-Fünfhaus'),
    ('1160, Ottakring'),
    ('1170, Hernals'),
    ('1180, Währing'),
    ('1190, Döbling'),
    ('1200, Brigittenau'),
    ('1210, Floridsdorf'),
    ('1220, Donaustadt'),
    ('1230, Liesing'),   
    )

    from faker import Faker
    from .models import User
    fake = Faker()
    for _ in range(150):
        user = User.objects.create_user(username=fake.user_name(),password='password',email=fake.email(),first_name=fake.first_name(), last_name=fake.last_name(), district=random.choice(DISTRICTS))
        user.save()
        print(user)

def generate_books():

    CATEGORIES_SET = (
        'Adventure',
        'Art',
        'Children',
        'Cooking',
        'Families & Relationships',
        'Fantasy',
        'Guide, How-to',
        'Health',
        'Historical fiction',
        'History',
        'Horror',
        'Humor',
        'Memoir',
        'Mystery',
        'Paranormal',
        'Philosophy',
        'Psychology',
        'Romance',
        'Science Fiction',
        'Self-help',
        'Thriller',
        'Travel',
        'Unknown',
    )

    CATEGORIES_SET_SLUG = (
    'adventure',
    'art',
    'children',
    'cooking',
    'families-relationships',
    'fantasy',
    'guide-how-to',
    'health',
    'historical-fiction',
    'history',
    'horror',
    'humor',
    'memoir',
    'mystery',
    'paranormal',
    'philosophy',
    'psychology',
    'romance',
    'science-fiction',
    'self-help',
    'thriller',
    'travel',
    'unknown',
)

    BOOK_LANGUAGE = (
        'slovak',
        'english',
        'german',
        'czech',
        'russian'
    )

    from faker import Faker
    from .models import User, Book
    fake = Faker()
    for _ in range(700):
        book = Book.objects.create(
            user_id = random.randint(1,355),
            title=fake.company(),
            author = fake.name(),
            price = random.randint(1,200),
            ISBN = fake.isbn10(),
            language = random.choice(BOOK_LANGUAGE),
            category = random.choice(CATEGORIES_SET_SLUG)
        )
        book.save()
        print(book)

def generate_offers():
    from faker import Faker
    from .models import User, Book, BookSellers
    fake = Faker()
    for _ in range(100):
        offer = BookSellers.objects.create(
            user_id = random.randint(163,284),
            book_id = random.randint(13,24),
            price = random.randint(0,100)
        )
        offer.save()
        print(offer)