import pandas as pd
import requests
import numpy as np
from comicBookMaster import Book
from bs4 import BeautifulSoup
import sys


def soup_finder(url_name, excel_name):
    payload = {'userSignInFormEmail': 'spswatron@yahoo.com', 'user_password': 'eternallove'}
    url = "https://www.goodreads.com/user/sign_in?source=home"
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
        }
        p = s.post(url, data=payload, headers=headers)
        # print the html returned or something more intelligent to see if it's a successful login page.
        # An authorised request.
        r = s.get(url_name)
        page = s.get('https://www.goodreads.com/shelf/show/comics?page=2')
        ans = page.status_code
        ans2 = s.cookies
        soup = BeautifulSoup(page.text, 'html.parser')
        next = soup.find('a', class_='next_page')['href']

        def page_sequence(url: str, page_num: int, book_list: list, i: int):
            if page_num < 2:
                page = s.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                books = soup.find_all('div', class_='elementList')

                def average_fix(start: str):
                    return start[len(start) - 5:]

                def represents_int(s):
                    try:
                        int(s)
                        return True
                    except ValueError:
                        return False

                def totals_fix(start: str):
                    help = list(start)
                    ans = []
                    for i in help:
                        if represents_int(i):
                            ans.append(i)
                    if "".join(ans) == "":
                        return 0
                    else:
                        return int("".join(ans))

                total = 0
                for book in books:
                    if total < 50:
                        i += 1
                        title = str(book.find('a', class_='bookTitle').get_text())
                        ratings = str(book.find('span', class_="greyText smallText")).split(">")[1].split("<")[0]
                        avgRating = average_fix(ratings.split("—")[0])
                        totalRatings = totals_fix(ratings.split("—")[1])
                        date = totals_fix(ratings.split("—")[2])
                        imgLink = book.find('img')['src']
                        actualLink = book.find('a', class_='bookTitle')['href']
                        writer = str(book.find('a', class_='authorName').text)
                        book_list.append(Book(i, title, avgRating, totalRatings, date, imgLink, actualLink, writer))
                        print(i)
                        total += 1

                next = soup.find('a', class_='next_page')['href']
                print("page " + str(page + 1))
                page_sequence(next, page_num + 1, book_list, i)

        book_list = []
        page_sequence(url_name, 0, book_list, 0)

    book_list = list(set(book_list))
    book_list.sort(reverse = True, key = lambda x : x.i)
    dict = {"i": map(lambda x: x.i, book_list),
            "title": map(lambda x: x.title, book_list),
            "avg review": map(lambda x: x.avg, book_list),
            "total reviews": map(lambda x: "{:,}".format(x.total), book_list),
            "publication": map(lambda x: x.published, book_list),
            "image link": map(lambda x: x.img, book_list),
            "actual link": map(lambda x: x.link, book_list),
            "author": map(lambda x: x.author, book_list)
            }

    brics = pd.DataFrame(dict)
    brics.index = np.arange(1, len(brics) + 1)
    brics.to_excel(sys.path[3] + '/data/' + excel_name + '.xlsx', index=False, engine='xlsxwriter')