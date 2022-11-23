import requests
import urllib
import csv
import time

"""
    Script to populate DB with Books from Google Books API 
"""

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
    ('humor', 'Humor'),
    ('political-science', 'Political Science'),
    ('social-science', 'Social Science'),
    ('sports-recreation', 'Sports & Recreation'),
    ('technology', 'Technology'),
    ('true-crime', 'True Crime'),
    ('unknown', 'Unknown'),
)

from .models import Book

def populateMe():
    with open('./isbn10_full.csv') as file:
        reader = csv.reader(file)
        id = 4638
        for isbn in reader:
            
            print('sleeping 40 for the first time...')
            time.sleep(30)
            try:
                # url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn[0]}&fields=items(id,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers,volumeInfo/description)&key=AIzaSyDjrM5K4xzt7p601ROtsFAY7ZftORmBnsQ'
                # url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn[0]}&fields=items(id,volumeInfo/description,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers)&key=AIzaSyBmYVEppv1Lseiu0wt7YGr-VbXoMraULiw'
                url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn[0]}&fields=items(id,volumeInfo/description,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers)&key=AIzaSyCdjm_QYo4osDiS8MJkjyLNx1PhoObkC5M'
                status = requests.get(url)
                print(f'STATUS 1st: {status}')
                if status.json() == {}:
                    print('sleeping 40 for the second time...')
                    time.sleep(30)
                    print('yes its empty, using another url')
                    # url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:0{isbn[0]}&fields=items(id,volumeInfo/description,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers)&key=AIzaSyDjrM5K4xzt7p601ROtsFAY7ZftORmBnsQ'
                    # url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:0{isbn[0]}&fields=items(id,volumeInfo/description,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers)&key=AIzaSyCnGQNvQvolKrmpyJ90Lr2cQ3cXfj-OBLU'
                    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:0{isbn[0]}&fields=items(id,volumeInfo/description,volumeInfo/authors,volumeInfo/imageLinks/smallThumbnail,volumeInfo/categories,volumeInfo/title,volumeInfo/language,volumeInfo/pageCount,volumeInfo/publishedDate,volumeInfo/subtitle,volumeInfo/industryIdentifiers)&key=AIzaSyBmyJbLnMiARTSjTLhdhMbxnMz7fNFhlB8'
                    status = requests.get(url)
                    print(f'STATUS 2nd: {status}')
                data = status.json()
                
                if data:
                    
                    # print(data)

                    if data['items'][0]['id']:
                        identifier = data['items'][0]['id']
                    else:
                        identifier = '000'

                    if data['items'][0]['volumeInfo']['title']:
                        title = data['items'][0]['volumeInfo']['title']
                    else:
                        title = 'Unknown'

                    if data['items'][0]['volumeInfo']['authors']:
                        authors = data['items'][0]['volumeInfo']['authors']
                        author = ''
                        if len(authors) == 1:
                            author =  authors[0]
                        else:
                            author = ', '.join(authors)
                    else:
                        author = 'Unknown'

                    if data['items'][0]['volumeInfo']['industryIdentifiers']:
                        for row in data['items'][0]['volumeInfo']['industryIdentifiers']:
                            if row['type'] == 'ISBN_13':
                                ISBN = row['identifier']
                    else:
                        ISBN = '000'

                    if data['items'][0]['volumeInfo']['language']:         
                        if data['items'][0]['volumeInfo']['language'] == 'en':
                           language = 'english'
                        elif data['items'][0]['volumeInfo']['language'] == 'de':
                            langauge = 'german'
                        elif data['items'][0]['volumeInfo']['language'] == 'es':
                            langauge = 'spanish'
                        elif data['items'][0]['volumeInfo']['language'] == 'fr':
                            langauge = 'french'
                        elif data['items'][0]['volumeInfo']['language'] == 'it':
                            langauge = 'italian'
                        else:
                            language = data['items'][0]['volumeInfo']['language']
                    else:
                        language = ''

                    if data['items'][0]['volumeInfo']['categories']:  
                        for cat in NEW_CATEGORIES:
                            if data['items'][0]['volumeInfo']['categories'][0] == cat[1]:    
                                category = cat[0]
                    else:
                        category = 'unknown'
                    
                    if data['items'][0]['volumeInfo']['pageCount']:
                        pages = data['items'][0]['volumeInfo']['pageCount']

                    if data['items'][0]['volumeInfo']['publishedDate']:
                        date_published = data['items'][0]['volumeInfo']['publishedDate']
                    
                    if 'description' in data['items'][0]['volumeInfo']:
                        description = data['items'][0]['volumeInfo']['description']
                    else:
                        description = ''

                    
                    imgURL = data['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
        
                    # print(id, title, author, ISBN, language, pages, date_published, category, description, identifier, cover)
                    id += 1
                    if imgURL:
                        with open(f'/media/{id}.jpg', 'wb') as coverIMG:
                                coverIMG.write(urllib.request.urlopen(imgURL).read())
                                cover = f'{id}.jpg'

                    new = Book.objects.create(id=id, title=title, author=author, ISBN=ISBN, language=language, category=category, page_count=pages, published_year=date_published, cover=cover, identifier=identifier, description=description)
                    new.save()

                    print(f'Book with ID: {id} successfully added to DB. Last added book ISBN: {isbn}')
                else:
                    print('{}')
            except Exception as e:
                print(f'error: {e}')
