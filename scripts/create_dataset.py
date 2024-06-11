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

def getFilmRating(session, tconst):
    rating = session.query(TitleRatings).filter_by(tconst=tconst).first()
    return rating

session = Session(engine)

films_ratings = session.query(TitleBasics).join(TitleRatings, TitleBasics.tconst == TitleRatings.tconst).with_entities(TitleBasics.tconst, TitleRatings.numVotes).all()

elements = []
probabilities = []
count = 0

print('[*] summing number of votes...')
for x in tqdm(films_ratings):
    count += int(x.numVotes)

print('[*] computing films probabilities...')
for x in tqdm(films_ratings):
    elements.append(x.tconst)
    probabilities.append(int(x.numVotes) / count)

print("[*] sampling a film list...")
with open('film_list.txt', 'w') as f:
    for film in tqdm(np.random.choice(elements, NUM_ELEMENTS, p=probabilities)):
        f.write(film + '\n')

