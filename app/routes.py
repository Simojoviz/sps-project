from flask import render_template, redirect, request
from app import app
from app.models import *
import time
import os

basedir = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = f'{basedir}/../data/log_db_time_1.csv'
open(LOG_FILE, 'w').close()


count = 1

def log_db_time(route, delta):
    global count
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{count},{delta},{route}\n")
        count +=1

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        form = request.form
        film = form.get('title')
        return redirect("/index/"+film)
    else:
        log_db_time('/', 0)
        return render_template('index.html', title='Home')


@app.route('/index/<_title>')
def film_page(_title):

    # DB start
    start_time = time.time()
    film = getFilmByTitle(_title)
    end_time = time.time()
    # DB end
    delta = end_time - start_time

    if film is None:
        log_db_time('/index', round(delta, 3))
        return "No film found"
    
    # DB start
    start_time = time.time()
    rating = getFilmRating(film.tconst)
    crew = getCrewByFilmId(film.tconst)
    end_time = time.time()
    # DB end
    delta += end_time - start_time

    average_rating = rating.averageRating if rating is not None else None
    film_duration = film.runtimeMinutes
    directors = []
    writers = []
    if crew is not None:
        t = 0
        for x in crew.directors.split(','):
            d = getCrewPersonById(x)
            t += d[1]
            if d[0] is not None:
                directors.append(d[0])

        for x in crew.writers.split(','):
            w = getCrewPersonById(x)
            t += w[1] #time for the query
            if w[0] is not None:
                writers.append(w[0])
        delta += t


    # DB start
    start_time = time.time()
    actors = getActorsByFilmId(film.tconst)
    end_time = time.time()
    # DB end
    delta += end_time - start_time
    
    log_db_time('/index', round(delta, 3))
    return render_template('film.html', film=film, directors=[d.primaryName for d in directors],
                            writers=[w.primaryName for w in writers], 
                            actors=[a.primaryName for a in actors], average_rating=average_rating, film_duration=film_duration)


@app.route('/actor/<_name>')
def actor_page(_name):
    # DB start
    start_time = time.time()
    actor = getPersonByName(_name)
    end_time = time.time()
    # DB end
    delta = end_time - start_time
    if actor is None:
        log_db_time('/actor', round(delta, 3))
        return "No actor of actress found"

    # DB start
    start_time = time.time()
    films = getFilmsByActor(actor.nconst)
    end_time = time.time()
    # DB end
    delta += end_time - start_time

    log_db_time('/actor', round(delta, 3))
    return render_template('actor.html', actor=actor, films=films)