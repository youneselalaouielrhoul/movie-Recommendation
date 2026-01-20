import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# absolute path to use the "tmdb-movies.csv" file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'tmdb-movies.csv')
df = pd.read_csv(file_path)

# important features
if not df.empty:
    columns = ['original_title', 'genres', 'director']
    for feature in columns:
        df[feature] = df[feature].fillna('')
    df['important_features'] = df['original_title'] + ' ' + df['genres'] + ' ' + df['director']

    # similarity matrix 
    cm = CountVectorizer().fit_transform(df['important_features'])
    cs = cosine_similarity(cm)
    
    # lower case series for better searching
    df['original_title_lower'] = df['original_title'].str.lower()

def get_recommendations(title):
    if df.empty:
        return []
    
    title = title.lower().strip()
    
    if title not in df['original_title_lower'].values:
        return None

    # index of the movie that matches the title
    movie_index = df[df.original_title_lower == title].index[0]
    
    score = list(enumerate(cs[movie_index]))
    sorted_scores = sorted(score, key=lambda x: x[1], reverse=True)
    sorted_scores = sorted_scores[1:8]  # top 7 recommendations
    
    recommendations = []
    for item in sorted_scores:
        idx = item[0]
        recommendations.append(df.iloc[idx]['original_title'])
        
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    error = None
    movie_title = ''
    
    if request.method == 'POST':
        movie_title = request.form.get('movie', '')
        result = get_recommendations(movie_title)
        if result is not None:
            recommendations = result
        else:
            error = "Movie not found. Please check the spelling or try another title."
    
    return render_template('index.html', recommendations=recommendations, error=error, movie_title=movie_title)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query or df.empty:
        return jsonify([])
    
    # Filter movies that contain the query string in their title
    matches = df[df['original_title_lower'].str.contains(query, na=False)]
    
    # top 10 matches
    suggestions = matches['original_title'].head(10).tolist()
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
