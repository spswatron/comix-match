from flask import *
from flask_bootstrap import Bootstrap
from file_processing import *
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='yo')
Bootstrap(app)


categories = [('home', 'comics'), ('CGN', 'comics, graphic novels, manga'), ('manga', 'manga'), ('chicklit', 'chicklit')]
sorting = ['average(highest)', 'average(lowest)', 'total reviews', 'goodreads default', 'random']
option = ('comicPage', 'comics')
def fixed(lister, op):
    return filter(lambda x: x != op, lister)

def super_page(request, file, loc, cat, choice, rank = "average(highest)"):
    if request.method == 'POST':
        helper = request.form['sortBy']
        new_list = fixed(sorting, helper)
        return render_template('index.html', books=tupleFeeder(file, helper), loc=loc, categories=cat, choice=choice, sort=new_list, style=helper)
    else:
        return render_template('index.html', books=tupleFeeder(file, rank), loc = loc, categories=cat, choice=choice, sort=fixed(sorting, rank), style=rank)

@app.route("/", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def home(rank="average(highest)"):
    option = ('home', 'comics')
    return super_page(request, 'data/comics.xlsx', "/", filter(lambda x: x != option, categories), option, rank)

@app.route("/manga", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/manga/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def manga(rank="average(highest)"):
    option = ('manga', 'manga')
    return super_page(request, 'data/manga.xlsx', "/manga", filter(lambda x: x != option, categories), option, rank)

@app.route("/chicklit", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/chicklit/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def chicklit(rank="average(highest)"):
    option = ('chicklit', 'chicklit')
    return super_page(request, 'data/chicklit.xlsx', "/chicklit", filter(lambda x: x != option, categories), option, rank)

@app.route("/comics-graphic-novels-manga", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
@app.route("/comics-graphic-novels-manga/<rank>", strict_slashes=False, methods=['GET', 'POST', 'PUT'])
def CGN(rank="average(highest)"):
    option = ('CGN', 'comics, graphic novels, manga')
    return super_page(request, 'data/CGN.xlsx', "/comics-graphic-novels-manga", filter(lambda x: x != option, categories), option, rank)

@app.route("/redirect/<rank>", strict_slashes=False, methods = ['POST'])
def next(rank):
    return redirect(url_for(request.form['category'], rank = rank))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)