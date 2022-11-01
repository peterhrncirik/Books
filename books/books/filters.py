import django_filters
from django import forms
from .models import BookSellers, Watchlist

DISTRICTS = (
    ('1010', '1010, Innenstadt'),
    ('1020', '1020, Leopoldstadt'),
    ('1030', '1030, Landstraße'),
    ('1040', '1040, Wieden'),
    ('1050', '1050, Margareten'),
    ('1060', '1060, Mariahilf'),
    ('1070', '1070, Neubau'),
    ('1080', '1080, Josefstadt'),
    ('1090', '1090, Alsergrund'),
    ('1100', '1100, Favoriten'),
    ('1110', '1110, Simmering'),
    ('1120', '1120, Meidling'),
    ('1130', '1130, Hietzing'),
    ('1140', '1140, Penzing'),
    ('1150', '1150, Rudolfsheim-Fünfhaus'),
    ('1160', '1160, Ottakring'),
    ('1170', '1170, Hernals'),
    ('1180', '1180, Währing'),
    ('1190', '1190, Döbling'),
    ('1200', '1200, Brigittenau'),
    ('1210', '1210, Floridsdorf'),
    ('1220', '1220, Donaustadt'),
    ('1230', '1230, Liesing'),   
)

class BookFilter(django_filters.FilterSet):

    district = django_filters.ChoiceFilter(choices=DISTRICTS, lookup_expr='startswith', field_name='user__district', empty_label='All districts', widget=forms.Select(attrs={'class': 'form-control'}), label='')
    
    order = django_filters.OrderingFilter(
        fields=(
            ('date_added', 'newest'),
            ('book__title', 'title-az'),
            ('-book__title', 'title-za'),
            ('price', 'price-low'),
            ('-price', 'price-high'),
        ),
        field_labels={
            'date_added': 'newest',
            'book__title': 'title-az',
            '-book__title': 'title-za',
            'price': 'price-low',
            '-price': 'price-high',
        },
        choices=[
            ('newest', 'Newest'),
            ('title-az', 'Title A-Z'),
            ('title-za', 'Title Z-A'),
            ('price-low', 'Price: Low to High'),
            ('price-high', 'Price: High to Low'),
        ],
        label='',
        empty_label='Sort by',
    )

    class Meta:
        model = BookSellers
        fields = ['district']

        help_texts = {
            'district': None,
        }

class BookFilterWatchlist(django_filters.FilterSet):
    district = django_filters.ChoiceFilter(choices=DISTRICTS, lookup_expr='startswith', field_name='user__district', empty_label='All districts', widget=forms.Select(attrs={'class': 'form-control'}), label='')
    
    order = django_filters.OrderingFilter(
        fields=(
            ('date_added', 'newest'),
            ('book__title', 'title-az'),
            ('-book__title', 'title-za'),
        ),
        field_labels={
            'date_added': 'newest',
            'book__title': 'title-az',
            '-book__title': 'title-za',
        },
        choices=[
            ('newest', 'Newest'),
            ('title-az', 'Title A-Z'),
            ('title-za', 'Title Z-A'),
        ],
        label='',
        empty_label='Sortieren nach',
    )

    class Meta:
        model = Watchlist
        fields = ['district']

        help_texts = {
            'district': None,
        }