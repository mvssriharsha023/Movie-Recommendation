from flask import Flask, render_template, redirect, url_for, request
import numpy as np
import pandas as pd
import pickle
import bz2
import _pickle as cPickle

app = Flask(__name__)

popular_movies = pickle.load(open('popular_movies.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))
content = bz2.BZ2File('similarity.pbz2', 'rb')
similarity = cPickle.load(content)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('Home.html', titles = list(popular_movies['Title'].values), poster = list(popular_movies['Poster'].values), 
                           ratings = list(popular_movies['Ratings'].values), votes = list(popular_movies['Votes'].values), 
                           year = list(popular_movies['Year'].values))

@app.route('/recommend', methods = ['GET', 'POST'])
def recommend():
    movie_titles = []
    movie_posters = []
    movie_year = []
    movie_ratings = []
    movie_votes = []
    inputed = []
    message = ''
    if request.method == "POST":
        user_input = request.form.get('user_input')

        if user_input in list(movies['Title'].values):
            inputed = list(movies[movies['Title'] == user_input].drop_duplicates('Title').values[0])
            index = movies[movies['Title'] == user_input].index[0]
            recommended_movies = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])[1: 21]
            df = pd.DataFrame()
            for movie in recommended_movies:
                series = pd.Series(movies.iloc[movie[0]])
                df = df.append(series, ignore_index=True)
            df = df.sort_values(by='Ratings', ascending=False).head(12)
            df = df.reset_index().drop(columns=['index'], axis=1)
            movie_titles=list(df['Title'].values)
            movie_posters=list(df['Poster'].values)
            movie_year=list(df['Year'].values)
            movie_ratings=list(df['Ratings'].values)
            movie_votes=list(df['Votes'].values)
        else:
            message = 'Search for the exact title'
        
        
    
    return render_template('Recommend.html', movie_titles=movie_titles, movie_posters=movie_posters,
                           movie_year=movie_year, movie_ratings=movie_ratings, movie_votes=movie_votes, inputed=inputed, message=message)



if __name__ == '__main__':
    app.run(debug = True)