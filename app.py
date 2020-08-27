from flask import *
from flask_bootstrap import Bootstrap
from file_processing import *
import os
import datetime as dt
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='yo')
Bootstrap(app)


categories = [('home', 'comics'), ('chicklit', 'chicklit'), ('CGN', 'comics, graphic novels, manga'),
              ('GN', 'graphic novels'), ('manga', 'manga'), ('teenRomance', 'teen romance'),
              ('YA', 'young adult')]
sorting = ['average(highest)', 'average(lowest)', 'total reviews', 'goodreads default', 'random']
option = ('comicPage', 'comics')
def fixed(lister, op):
    return filter(lambda x: x != op, lister)

def super_page(request, file, loc, cat, choice, name, fav, shelf, rank = "average(highest)"):
    last_update = dt.datetime.fromtimestamp(os.path.getmtime(file))
    last_update = last_update.strftime("%m/%d/%Y")
    if request.method == 'POST':
        helper = request.form['sortBy']
        new_list = fixed(sorting, helper)
        return render_template('index.html', books=tupleFeeder(file, helper), loc=loc,
                               categories=cat, choice=choice, sort=new_list,
                               style=helper, favicon=fav, name=name, time = last_update,
                               shelf=shelf)
    else:
        return render_template('index.html', books=tupleFeeder(file, rank), loc = loc,
                               categories=cat, choice=choice, sort=fixed(sorting, rank),
                               style=rank, favicon=fav, name=name, time = last_update,
                               shelf=shelf)

@app.route("/", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def home(rank="average(highest)"):
    option = ('home', 'comics')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon.png"
    return super_page(request, 'data/comics.xlsx', "/",
                      filter(lambda x: x != option, categories), option, 'Comix',
                      'https://www.goodreads.com/shelf/show/comics', rank)

@app.route("/manga", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/manga/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def manga(rank="average(highest)"):
    option = ('manga', 'manga')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon-M.png"
    return super_page(request, 'data/manga.xlsx', "/manga",
                      filter(lambda x: x != option, categories), option, 'Manga',
                      'https://www.goodreads.com/shelf/show/mang%C3%A1', rank)

@app.route("/chicklit", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/chicklit/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def chicklit(rank="average(highest)"):
    option = ('chicklit', 'chicklit')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon.png"
    return super_page(request, 'data/chicklit.xlsx', "/chicklit",
                      filter(lambda x: x != option, categories), option, 'Chicklit', fav,
                      "https://www.goodreads.com/shelf/show/chick-lit", rank)

@app.route("/comics-graphic-novels-manga", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/comics-graphic-novels-manga/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def CGN(rank="average(highest)"):
    option = ('CGN', 'comics, graphic novels, manga')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon-M.png"
    return super_page(request, 'data/CGN.xlsx', "/comics-graphic-novels-manga",
                      filter(lambda x: x != option, categories), option, 'Mix', fav,
                      'https://www.goodreads.com/shelf/show/comics-graphic-novels-manga', rank)

@app.route("/teen-romance", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/teen-romance/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def teenRomance(rank="average(highest)"):
    option = ('teenRomance', 'teen romance')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon-T.png"
    return super_page(request, 'data/teen-romance.xlsx', "/teen-romance",
                      filter(lambda x: x != option, categories), option, 'Teen', fav,
                      'https://www.goodreads.com/shelf/show/teen-romance', rank)

@app.route("/young-adult", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/young-adult/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def YA(rank="average(highest)"):
    print(rank)
    option = ('YA', 'young adult')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon-y.png"
    return super_page(request, 'data/young-adult.xlsx', "/young-adult",
                      filter(lambda x: x != option, categories), option, 'YA', fav,
                      'https://www.goodreads.com/shelf/show/young-adult', rank)

@app.route("/graphic-novels", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/graphic-novels/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def GN(rank="average(highest)"):
    print(rank)
    option = ('GN', 'graphic novels')
    fav = "https://github.com/spswatron/files-for-comix-match/raw/master/apple-touch-icon-g.png"
    return super_page(request, 'data/graphic-novels.xlsx', "/graphic-novels",
                      filter(lambda x: x != option, categories), option, 'Graphics', fav,
                      'https://www.goodreads.com/shelf/show/graphic-novels', rank)

@app.route("/redirect/<rank>", strict_slashes=False, methods = ['POST'])
def next(rank):
    return redirect(url_for(request.form['category'], rank = rank))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)