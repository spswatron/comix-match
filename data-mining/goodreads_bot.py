from comicBookMaster import genre_find
from bs4_detector import soup_finder

# genre_find('https://www.goodreads.com/shelf/show/graphic-novels', 'graphic-novels')
# soup_finder('https://www.goodreads.com/shelf/show/comics', 'comics')

def update_all():
    genre_find('https://www.goodreads.com/shelf/show/comics', 'comics')
    genre_find('https://www.goodreads.com/shelf/show/graphic-novels', 'graphic-novels')
    genre_find('https://www.goodreads.com/shelf/show/comics-graphic-novels-manga', 'CGN')
    genre_find('https://www.goodreads.com/shelf/show/chicklit', 'chicklit')
    genre_find('https://www.goodreads.com/shelf/show/teen-romance', 'teen-romance')
    genre_find('https://www.goodreads.com/shelf/show/young-adult', 'young-adult')

update_all()