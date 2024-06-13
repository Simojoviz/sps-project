from flask import render_template, redirect, request
from app import app
from app.models import *
import time

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        form = request.form
        film = form.get('title')
        return redirect("/index/"+film)
    else:
        return render_template('index.html', title='Home')


@app.route('/index/<_title>')
def film_page(_title):

    # DB start
    start_time = time.time()
    film = getFilmByTitle(_title)
    if film is None:
        return "No film found"
    
    rating = getFilmRating(film.tconst)
    average_rating = rating.averageRating if rating is not None else None
    
    directors = getDirectorsByFilmId(film.tconst)
    writers = getWritersByFilmId(film.tconst)

    actors = getActorsByFilmId(film.tconst)
    end_time = time.time()
    # DB end
    db_time = round(end_time - start_time, 5)
   
    return render_template('film.html', film=film, directors=[d.primaryName for d in directors],
                            writers=[w.primaryName for w in writers], 
                            actors=[a.primaryName for a in actors], average_rating=average_rating)


@app.route('/actor/<_name>')
def actor_page(_name):
    
    # DB start
    start_time = time.time()
    actor = getPersonByName(_name)
    end_time=time.time()
    # DB end
    db_time = end_time-start_time

    if actor is None:
        return "No actor of actress found"

    # DB start
    start_time = time.time()
    films = getFilmsByActor(actor.nconst)
    end_time=time.time()
    # DB end
    db_time = round(db_time + end_time-start_time, 5)

    return render_template('actor.html', actor=actor, films=films)