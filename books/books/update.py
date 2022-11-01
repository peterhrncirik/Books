from .models import Book

def update():
    fantasy = Book.objects.filter(category='fantasy')
    if fantasy:
        for book in fantasy:
            book.category = 'unknown'
            book.save()
        print('Successfully updated books in Fantasy')

    bios = Book.objects.filter(category='biographies-memoirs')
    if bios:
        for book in bios:
            book.category = 'biography-autobiography'
            book.save()
        print('Successfully updated books in Bios')

    mystery = Book.objects.filter(category='mystery')
    if mystery:
        for book in mystery:
            book.category = 'unknown'
            book.save()
        print('Successfully updated books in Mystery')

    horror = Book.objects.filter(category='horror')
    if horror:
        for book in horror:
            book.category = 'drama'
            book.save()
        print('Successfully updated books in Horror')

    thriller = Book.objects.filter(category='thriller')
    if thriller:
        for book in thriller:
            book.category = 'true-crime'
            book.save()
        print('Successfully updated books in Thriller')

    paranormal = Book.objects.filter(category='paranormal')
    if paranormal:
        for book in paranormal:
            book.category = 'adventure'
            book.save()
        print('Successfully updated books in Paranormal')

    historical_fiction = Book.objects.filter(category='historical-fiction')
    if historical_fiction:
        for book in historical_fiction:
            book.category = 'fiction'
            book.save()
        print('Successfully updated books in Historical Fiction')

    science_fiction = Book.objects.filter(category='science-fiction')
    if science_fiction:
        for book in science_fiction:
            book.category = 'fiction'
            book.save()
        print('Successfully updated books in Science Fiction')

    memoir = Book.objects.filter(category='memoir')
    if memoir:
        for book in memoir:
            book.category = 'biography-autobiography'
            book.save()
        print('Successfully updated books in Memoir')

    education = Book.objects.filter(category='education-teaching')
    if education:
        for book in education:
            book.category = 'education'
            book.save()
        print('Successfully updated books in Education')

    health = Book.objects.filter(category='health')
    if health:
        for book in health:
            book.category = 'health-fitness'
            book.save()
        print('Successfully updated books in Health')

    guide = Book.objects.filter(category='guide-how-to')
    if guide:
        for book in guide:
            book.category = 'crafts-hobbies'
            book.save()
        print('Successfully updated books in Guide')

    family = Book.objects.filter(category='families-relationships')
    if family:
        for book in family:
            book.category = 'family-relationships'
            book.save()
        print('Successfully updated books in Family')

    children = Book.objects.filter(category='children')
    if children:
        for book in children:
            book.category = 'juvenile-fiction'
            book.save()
        print('Successfully updated books in Children')


