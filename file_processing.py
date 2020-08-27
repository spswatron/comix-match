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
        return dataFramer(file, lambda x: int(x['total reviews'].replace(",", "")), False, False)
    if selected == "goodreads default":
        return dataFramer(file, lambda x: x['i'], True, False)
    if selected == "random":
        return dataFramer(file, lambda x: x['title'], True, True)