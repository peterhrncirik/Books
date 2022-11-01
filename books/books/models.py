from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db import IntegrityError

CONDITION_CHOICES = (
    ('Newest', 'Newest'),
    ('Used', 'Used'),
    ('Old', 'Old'),
)

# CATEGORIES = (
#     ('biographien', 'Biographien'),
#     ('comics-mangas', 'Comics / Mangas'),
#     ('fachbuecher', 'Fachbücher'),
#     ('fantasy-science-fiction', 'Fantasy / Science Fiction'),
#     ('fitness-gesundheit', 'Fitness / Gesundheit'),
#     ('freizeit-hobby', 'Freizeit / Hobby'),
#     ('geschichte', 'Geschichte'),
#     ('humor-unterhaltung', 'Humor / Unterhaltung'),
#     ('klassiker-der-literatur', 'Klassiker der Literatur'),
#     ('krimis-thriller', 'Krimis / Thriller'),
#     ('liebe-romantik', 'Liebe / Romantik'),
#     ('lyrik-gedichte', 'Lyrik / Gedichte'),
#     ('reisefuehrer-reiseliteratur', 'Reiseführer / Reiseliteratur'),
#     ('romane-erzaehlungen', 'Romane / Erzählungen'),
#     ('sachbuecher', 'Sachbücher'),
#     ('sport', 'Sport'),
#     ('unbekannt', 'Unbekannt')
# )

NEW_CATEGORIES = (
    ('art', 'Art'),
    ('antiques-collectibles', 'Antiques & Collectibles'),
    ('architecture', 'Architecture'),
    ('psychology', 'Psychology'),
    ('philosophy', 'Philosophy'),
    ('adventure', 'Adventure'),
    ('romance', 'Romance'),
    ('biography-autobiography', 'Biography & Autobiography'),
    ('body-mind-spirit', 'Body, Mind & Spirit'),
    ('business-economics', 'Business & Economics'),
    ('computers', 'Computers'),
    ('crafts-hobbies', 'Crafts & Hobbies'),
    ('design', 'Design'),
    ('drama', 'Drama'),
    ('education', 'Education'),
    ('foreign-language-study', 'Foreign Language Study'),
    ('gardening', 'Gardening'),
    ('house-home', 'House & Home'),
    ('language-arts-disciplines', 'Language Arts & Disciplines'),
    ('law', 'Law'),
    ('mathematic', 'Mathematic'),
    ('pets', 'Pets'),
    ('photography', 'Photography'),
    ('religion', 'Religion'),
    ('science', 'Science'),
    ('fiction', 'Fiction'),
    ('non-fiction', 'Non-Fiction'),
    ('travel', 'Travel'),
    ('true-crime', 'True Crime'),
    ('games-activities', 'Games & Activities'),
    ('humor', 'Humor'),
    ('juvenile-fiction', 'Juvenile Fiction'),
    ('juvenile-nonfiction', 'Juvenile Nonfiction'),
    ('medical', 'Medical'),
    ('cooking', 'Cooking'),
    ('self-help', 'Self-help'),
    ('music', 'Music'),
    ('health-fitness', 'Health & Fitness'),
    ('history', 'History'),
    ('nature', 'Nature'),
    ('performing-arts', 'Performing Arts'),
    ('poetry', 'Poetry'),
    ('family-relationships', 'Family & Relationships'),
    ('political-science', 'Political Science'),
    ('social-science', 'Social Science'),
    ('sports-recreation', 'Sports & Recreation'),
    ('technology', 'Technology'),
    ('unknown', 'Unknown'),
)

DISTRICTS = (
    ('1010, Innenstadt', '1010, Innenstadt'),
    ('1020, Leopoldstadt', '1020, Leopoldstadt'),
    ('1030, Landstraße', '1030, Landstraße'),
    ('1040, Wieden', '1040, Wieden'),
    ('1050, Margareten', '1050, Margareten'),
    ('1060, Mariahilf', '1060, Mariahilf'),
    ('1070, Neubau', '1070, Neubau'),
    ('1080, Josefstadt', '1080, Josefstadt'),
    ('1090, Alsergrund', '1090, Alsergrund'),
    ('1100, Favoriten', '1100, Favoriten'),
    ('1110, Simmering', '1110, Simmering'),
    ('1120, Meidling', '1120, Meidling'),
    ('1130, Hietzing', '1130, Hietzing'),
    ('1140, Penzing', '1140, Penzing'),
    ('1150, Rudolfsheim-Fünfhaus', '1150, Rudolfsheim-Fünfhaus'),
    ('1160, Ottakring', '1160, Ottakring'),
    ('1170, Hernals', '1170, Hernals'),
    ('1180, Währing', '1180, Währing'),
    ('1190, Döbling', '1190, Döbling'),
    ('1200, Brigittenau', '1200, Brigittenau'),
    ('1210, Floridsdorf', '1210, Floridsdorf'),
    ('1220, Donaustadt', '1220, Donaustadt'),
    ('1230, Liesing', '1230, Liesing'),   
)

RATINGS = (
    ('good', 'Satisfied'),
    ('medium', 'Okay'),
    ('bad', 'Unsatisfied'),
)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_private = models.BooleanField(default=False)
    about_me = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=40, choices=DISTRICTS, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    rating_good = models.IntegerField(default=0)
    rating_medium = models.IntegerField(default=0)
    rating_bad = models.IntegerField(default=0)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField()

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'


class Book(models.Model):
    title = models.CharField('title', max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    author = models.CharField('author', max_length=200)
    ISBN = models.CharField('ISBN', max_length=20)
    language = models.CharField('language', max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.CharField('category', max_length=40, choices=NEW_CATEGORIES, default='unknown')
    cover = models.ImageField(null=True, blank=True, default="no_img.gif")
    page_count = models.CharField('pagenumber', max_length=6, null=True, blank=True)
    published_year = models.CharField('year', max_length=5, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    identifier = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Book ID: {self.id} | Title: {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('book', args=[self.id, self.slug])
        
    class Meta:
        ordering = ['-date_added']

class BookSellers(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=8, choices=CONDITION_CHOICES, default='Used')
    additional_info = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    sold_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='sold_to')
    
    def __str__(self):
        return f'{self.book} | Seller: {self.user}'
    
    class Meta:
        ordering = ['-date_added']

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'User: {self.user} | Book: {self.book}'

class Ratings(models.Model):
   user_rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rated')
   user_rating = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
   book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
   rating = models.CharField(max_length=10, choices=RATINGS, default='good')
   comment = models.TextField(max_length=500, null=True, blank=True)
   date = models.DateTimeField(auto_now_add=True, null=True, blank=True)



