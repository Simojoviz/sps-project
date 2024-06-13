from sqlalchemy import Column, Integer, Boolean, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session
from tqdm import tqdm
import os
import numpy as np

NUM_ELEMENTS= 10000


basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine(f'sqlite:///{basedir}/../data/database.sqlite3', echo=False)

Base = declarative_base()
    
class TitleBasics(Base):
    __tablename__ = 'title_basics'

    tconst = Column(String(200), primary_key=True)
    titleType = Column(String(500) )
    primaryTitle = Column(String(500))
    originalTitle = Column(String(500))
    isAdult = Column(Boolean)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(String(500))
    genres = Column(String(500))

    def __repr__(self):
        obj = {
            "tconst" : self.tconst,
            "titleType" : self.titleType,
            "primaryTitle" : self.primaryTitle,
            "originalTitle" : self.originalTitle,
            "isAdult" : self.isAdult,
            "startYear" : self.startYear,
            "endYear" : self.endYear,
            "runtimeMinutes" : self.runtimeMinutes,
            "genres" : self.genres
        }
        return 'TitleBasics {}'.format(obj)
    
class TitleRatings(Base):

    __tablename__ = 'title_ratings'
    
    tconst = Column(String(200), primary_key=True)
    averageRating = Column(Float)
    numVotes = Column(Integer)    
    
    def __repr__(self):
        return '<TitleRatings {}>'.format(self.averageRating)
    

class TitlePrincipals(Base):

    __tablename__ = 'title_principals'

    tconst = Column(String(200), primary_key=True)
    ordering = Column(Integer, primary_key=True)
    nconst = Column(String(200))
    category = Column(String(200))
    job = Column(String(200))
    characters = Column(String(200))

    def __repr__(self):
        return '<TitlePrincipals {}>'.format(self.tconst)
    

class NameBasics(Base):

    __tablename__ = 'name_basics'

    nconst = Column(String(200), primary_key=True)
    primaryName = Column(String(200))
    birthYear = Column(Integer)
    deathYear = Column(Integer)
    primaryProfession = Column(String(500))
    knownForTitles = Column(String(500))
    
    
    def __repr__(self):
        obj = {
            "nconst" :  self.nconst,
            "primaryName" :  self.primaryName,
            "birthYear" :  self.birthYear,
            "deathYear" :  self.deathYear,
            "primaryProfession" :  self.primaryProfession,
            "knownForTitles" :  self.knownForTitles
        }
        return 'NameBasics {}'.format(obj)


def getFilmRating(session, tconst):
    rating = session.query(TitleRatings).filter_by(tconst=tconst).first()
    return rating

def getActorsByFilmId(session, tconst):
    actors = session.query(TitlePrincipals).filter((TitlePrincipals.tconst==tconst) & ((TitlePrincipals.category == 'actor') | (TitlePrincipals.category == 'actress'))) \
                                  .join(NameBasics, TitlePrincipals.nconst == NameBasics.nconst).with_entities(NameBasics) \
                                  .first()
    return actors


session = Session(engine)

films_ratings = session.query(TitleBasics).join(TitleRatings, TitleBasics.tconst == TitleRatings.tconst) \
                                          .with_entities(TitleBasics.tconst, TitleBasics.primaryTitle, TitleRatings.numVotes).all()

elements = []
probabilities = []
count = 0

print('[*] summing number of votes...')
for x in tqdm(films_ratings):
    count += int(x.numVotes)

print('[*] computing films probabilities...')
for x in tqdm(films_ratings):
    elements.append((x.tconst, x.primaryTitle))
    probabilities.append(int(x.numVotes) / count)


print("[*] sampling a film list...")
with open('../data/film_actor_list.csv', 'w') as f:
    for i in tqdm(np.random.choice(len(elements), NUM_ELEMENTS, p=probabilities)):
        film = elements[i]
        actor = getActorsByFilmId(session, film[1])
        f.write(f'{film[0]},{actor}\n')

