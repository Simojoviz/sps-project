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
        print(film)
        return redirect("/index/"+film)

    return render_template('index.html', title='Home', form=form)


@app.route('/index/<_title>')
def film_page(_title):
    film = getFilmByTitle(_title)
    crew = getCrewByFilmId(film.tconst) if film is not None else {}
    res = ""
    if film:
        res = f'<p> {str(film)} </p>\n<p> {str(crew)} </p>'
    else:
        res = "No film found"    
    return res

   