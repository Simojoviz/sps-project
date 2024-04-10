from app import db

class TitleCrew(db.Model):
    tconst = db.Column(db.String(500), primary_key=True)
    directors = db.Column(db.String(50000))
    writers = db.Column(db.String(50000))

    def __repr__(self):
        return '<TitleCrew {}>'.format(self.username)
    


# per ora non importato
class TitleAkas(db.Model):
    
    titleId = db.Column(db.String(500), primary_key=True)
    ordering = db.Column(db.Integer )
    title = db.Column(db.String(500))
    region = db.Column(db.String(500))
    language = db.Column(db.String(500))
    types = db.Column(db.String(500))
    attributes = db.Column(db.String(500))
    isOriginalTitle = db.Column(db.Boolean)

    def __repr__(self):
        return '<TitleAkas {}>'.format(self.username)
    

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
        return '<TitleBasics {}>'.format(self.primaryTitle)


def getFilmByTitle(title):
    films = TitleBasics.query.filter_by(primaryTitle = title).first()
    print("query eseguita")
    return films


class TitleEpisode(db.Model):
    tconst = db.Column(db.String(200), primary_key=True)
    parentTconst = db.Column(db.String(200))
    seasonNumber = db.Column(db.Integer)
    episodeNumber = db.Column(db.Integer)
    
    def __repr__(self):
        return '<TitleEpisode {}>'.format(self.tconst)
    

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
        return '<NameBasics {}>'.format(self.primaryName)
    