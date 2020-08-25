from flask import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from file_processing import *
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ysuixeryqefywk:dab2fb532443ee29056d25b0a2c19455001a7bccc24fbec706ed68565c979e7e@ec2-34-200-15-192.compute-1.amazonaws.com:5432/d67qv5uuekkqlp'

db = SQLAlchemy(app)
app.config.from_mapping(
    SECRET_KEY='yo')
Bootstrap(app)

def super_page(request, file, loc):
    if request.method == 'POST':
        return render_template('index.html', books=tupleFeeder(file, request.form['sortBy']), loc=loc)
    return render_template('index.html', books=dataFramer(file, None, None, None), loc = loc)

# xyz = super_page(None, '/Users/ashleychang/Documents/CSInstalls/goodreadsAnalysis/comics.xlsx', '/')
# yhl = 0

@app.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return super_page(request, '/Users/ashleychang/PycharmProjects/BBPlus/goodreads/directoryWebsite/data/comics.xlsx', "/")


@app.route("/comics", methods=['GET', 'POST', 'PUT'])
def comicPage():
    return super_page(request, '/Users/ashleychang/PycharmProjects/BBPlus/goodreads/directoryWebsite/data/comics.xlsx', "/comics")


@app.route("/redirect", methods = ['POST'])
def next():
    return redirect(url_for(request.form['category']))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
