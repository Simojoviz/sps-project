from flask import render_template, redirect, request
from app import app
from app.models import *

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
    film = getFilmByTitle(_title)
    if film is None:
        return "No film found"
    
    rating = getFilmRating(film.tconst)
    average_rating = rating.averageRating if rating is not None else None
    crew = getCrewByFilmId(film.tconst)
    directors = []
    writers = []
    if crew is not None:
        directors = filter(lambda x: x is not None, [getPersonById(d) for d in crew.directors.split(',')])
        writers = filter(lambda x: x is not None, [getPersonById(w) for w in crew.writers.split(',')])

    actors = getActorsByFilmId(film.tconst)
   
    return render_template('film.html', film=film, directors=[d.primaryName for d in directors],
                            writers=[w.primaryName for w in writers], 
                            actors=[a.primaryName for a in actors], average_rating=average_rating)


@app.route('/actor/<_name>')
def actor_page(_name):
    actor = getPersonByName(_name)
    if actor is None:
        return "No actor of actress found"

    films = getFilmsByActor(actor.nconst)

    return render_template('actor.html', actor=actor, films=films)