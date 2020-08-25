import pandas as pd
import numpy as np
import locale


def dataFramer(file, function, ascending, random):
    df = pd.read_excel(file)
    if function == None:
        df = df.sort_values(by=['avg review'], ascending=ascending)
    elif random:
        df = df.sample(frac=1).reset_index(drop=True)
    else:
        df['measure'] = df.apply(function, axis=1)
        df.sort_values(by=['measure'], inplace=True, ascending=ascending)
    df.index = np.arange(1, len(df) + 1)
    return np.array(df.to_records(index=True))


def tupleFeeder(file, selected):
    if selected == "average(highest)":
        return dataFramer(file, lambda x: x['avg review'], False, False)
    if selected == "average(lowest)":
        return dataFramer(file, lambda x: x['avg review'], True, False)
    if selected == "total reviews":
        return dataFramer(file, lambda x: locale.atoi(x['total reviews']), False, False)
    if selected == "goodreads default":
        return dataFramer(file, lambda x: x['i'], True, False)
    if selected == "random":
        return dataFramer(file, lambda x: x['title'], True, True)

x= tupleFeeder("/Users/ashleychang/Documents/CSInstalls/goodreadsAnalysis/comics.xlsx", 'random')
y = 0

# class book_list(db.Model):
#     rank = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     average = db.Column(db.Integer, nullable=False)
#     total = db.Column(db.Integer, nullable=False)
#     published = db.Column(db.Integer, nullable=True)
#     average = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return self.id
#
#
# class Form(FlaskForm):
#     sortBy = SelectField('sort by', choices = ["average(highest)", "average(lowest)", "total reviews", "goodreads default"])
