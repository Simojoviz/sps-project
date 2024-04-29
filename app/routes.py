from flask import render_template, redirect
from app import app
from app.forms import SearchForm
from app.models import *

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    form = SearchForm()
    if form.validate_on_submit():
        film = form.title.data
        return redirect("/index/"+film)

    return render_template('index.html', title='Home', form=form)


@app.route('/index/<_title>')
def film_page(_title):
    film = getFilmByTitle(_title)
    if film is None:
        return "No film found"
     
    crew = getCrewByFilmId(film.tconst)
    directors = []
    writers = []
    if crew is not None:
        directors = [getPersonById(d) for d in crew.directors.split(',')]
        writers = [getPersonById(w) for w in crew.writers.split(',')]

    principals = getPrincipalsByFilmId(film.tconst)
    actors = []
    if principals is not None:
        actors = [getPersonById(p.nconst) for p in filter(lambda x: x.category == 'actor' or x.category == 'actress', principals)]
    return render_template('film.html', film=film, directors=[d.primaryName for d in directors],
                            writers=[w.primaryName for w in writers], 
                            actors=[a.primaryName for a in actors], average_rating=7)
