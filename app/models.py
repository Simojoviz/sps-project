from app import db

class TitleAkas(db.Model):
    
    titleId = db.Column(db.String(500), primary_key=True)
    ordering = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(500))
    region = db.Column(db.String(500))
    language = db.Column(db.String(500))
    types = db.Column(db.String(500))
    attributes = db.Column(db.String(500))
    isOriginalTitle = db.Column(db.Boolean)

    def __repr__(self):
        obj = {
            "titleId" : self.titleId, 
            "ordering" : self.ordering,
            "title" : self.title,
            "region" : self.region,
            "language" : self.language,
            "types" : self.types,
            "attributes" : self.attributes,
            "isOriginalTitle" : self.isOriginalTitle
        }
        return 'TitleAkas {}'.format(obj)
    

class TitleBasics(db.Model):
    tconst = db.Column(db.String(200), primary_key=True)
    titleType = db.Column(db.String(500) )
    primaryTitle = db.Column(db.String(500))
    originalTitle = db.Column(db.String(500))
    isAdult = db.Column(db.Boolean)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.String(500))
    genres = db.Column(db.String(500))

   
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

class TitleCrew(db.Model):
    tconst = db.Column(db.String(500), primary_key=True)
    directors = db.Column(db.String(50000))
    writers = db.Column(db.String(50000))

    def __repr__(self):
        obj = {
            "tconst" :  self.tconst,
            "directors" :  self.directors,
            "writers" :  self.writers
        }
        return 'TitleCrew {}'.format(obj)


class TitleEpisode(db.Model):
    tconst = db.Column(db.String(200), primary_key=True)
    parentTconst = db.Column(db.String(200))
    seasonNumber = db.Column(db.Integer)
    episodeNumber = db.Column(db.Integer)
    
    def __repr__(self):
        return '<TitleEpisode {}>'.format(self.tconst)
    
class TitlePrincipals(db.Model):
    tconst = db.Column(db.String(200), primary_key=True)
    ordering = db.Column(db.Integer, primary_key=True)
    nconst = db.Column(db.String(200))
    category = db.Column(db.String(200))
    job = db.Column(db.String(200))
    characters = db.Column(db.String(200))

    def __repr__(self):
        return '<TitlePrincipals {}>'.format(self.tconst)
    

class TitleRatings(db.Model):
    
    tconst = db.Column(db.String(200), primary_key=True)
    averageRating = db.Column(db.Float)
    numVotes = db.Column(db.Integer)
    
    
    def __repr__(self):
        return '<TitleRatings {}>'.format(self.averageRating)
    

class NameBasics(db.Model):
    nconst = db.Column(db.String(200), primary_key=True)
    primaryName = db.Column(db.String(200))
    birthYear = db.Column(db.Integer)
    deathYear = db.Column(db.Integer)
    primaryProfession = db.Column(db.String(500))
    knownForTitles = db.Column(db.String(500))
    
    
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
    
def getFilmByTitle(title):
    filmAkas = TitleAkas.query.filter_by(title=title).first()
    if filmAkas is not None:
        film = TitleBasics.query.filter_by(tconst=filmAkas.titleId).first()
        return film
    else:
        return None

def getAkasByFilmId(tconst):
    aka = TitleAkas.query.filter_by(titleId=tconst).all()
    return aka

def getCrewByFilmId(tconst):
    crew = TitleCrew.query.filter_by(tconst=tconst).first()
    return crew

def getPrincipalsByFilmId(tconst):
    principals = TitlePrincipals.query.filter_by(tconst=tconst).all()
    return principals

def getPersonById(nconst):
    person = NameBasics.query.filter_by(nconst=nconst).first()
    return person

