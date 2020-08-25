import pandas as pd
import numpy as np
import sys
from selenium import webdriver


class Book:
    def __init__(self, i, title: str, avg: int, total: int, published: int, img: str, link: str, author: str):
        self.i = i
        self.title = title
        self.avg = avg
        self.total = total
        self.published = published
        self.img = img
        self.link = link
        self.author = author

    def __hash__(self):
        return hash(self.link)

    def __eq__(self, other):
        if isinstance(other, Book):
            part1 = self.title == other.title and self.avg == other.avg
            part2 = self.total == other.total and self.published == other.published
            part3 = self.img == other.img and self.link == other.link
            return part1 and part2 and part3 and self.author == other.author
        return False

def genre_find(url_name, excel_name):
    x = sys.path
    y= sys.path[3] + '/data/' + excel_name + '.xlsx'
    z=0
    driver = webdriver.Chrome(executable_path = '/Users/ashleychang/Documents/CSInstalls/selenium/chromedriver')


    def goodreads_login():
        driver.get("https://www.goodreads.com/")
        driver.find_element_by_id("userSignInFormEmail").send_keys("spswatron@yahoo.com")
        driver.find_element_by_id ("user_password").send_keys("eternallove")
        driver.find_element_by_xpath('//*[@id="sign_in"]/div[3]/input[1]').click()


    goodreads_login()


    def page_sequence(url: str, page_num: int, book_list: list, i: int):
        if page_num < 2:
            driver.get(url)
            books = driver.find_elements_by_class_name('elementList')

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


            for book in books:
                i += 1
                all = str(book.text).split("\n")
                if len(all) >= 3:
                    title = all[0]
                    ratings = all[2]
                    avgRating = average_fix(ratings.split("—")[0])
                    totalRatings = totals_fix(ratings.split("—")[1])
                    date = totals_fix(ratings.split("—")[2])
                    imgLink = str(book.find_element_by_tag_name('img').get_attribute('src'))
                    actualLink = str(book.find_element_by_class_name("bookTitle").get_attribute('href'))
                    writer = str(book.find_element_by_class_name('authorName').text)
                    book_list.append(Book(i, title, avgRating, totalRatings, date, imgLink, actualLink, writer))

            next = driver.find_element_by_class_name('next_page')
            next_url = str(next.get_attribute('href'))
            page_sequence(next_url, page_num + 1, book_list, i)

    book_list = []
    page_sequence(url_name, 0, book_list, 0)
    driver.quit()
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