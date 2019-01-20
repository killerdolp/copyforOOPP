from flask import Flask,render_template,request,flash,redirect,url_for,session
from wtforms import Form,StringField,FileField,validators,TimeField,DateField,IntegerField
from flask_uploads import UploadSet,configure_uploads,IMAGES

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class Tournament(Base):
    __tablename__="tournament"

    id= Column('id',Integer,primary_key=True)
    tournamentName=Column('TournamentName',String)
    time1=Column('time1',String)
    time2=Column('time2',String)
    date=Column('date',String)
    place=Column('place',String)
    betting_amount=Column('betting_amount',String)
    filename=Column('filename',String)

    def __init__(self,tournamentName,time1,time2,date,place,betting_amount,filename):
        self.tournamentName=tournamentName
        self.time1=time1
        self.time2=time2
        self.date=date
        self.place=place
        self.betting_amount=betting_amount
        self.filename=filename

    def get_id(self):
        return self.id

    def get_tournamentName(self):
        return self.tournamentName

    def get_time1(self):
        return self.time1

    def get_time2(self):
        return self.time2

    def get_date(self):
        return self.date

    def get_place(self):
        return self.place

    def get_betting_amount(self):
        return self.betting_amount

    def get_filename(self):
        return self.filename


engine = create_engine('sqlite:///match.db',echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
list=[]
def matchdb_retrieve():
    global list
    list.clear()
    session = Session()
    matches = session.query(Tournament).all()
    for match in matches:
        list.append(match)
    session.close()
    return len(list)


x=0
app = Flask(__name__)

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app, photos)


@app.route('/')
@app.route('/<user>')
def user(user=None):
    return render_template("Homepage.html" ,user=user)


class CreateTournament(Form):

    Tournament_Name = StringField("Tournament Name", [validators.Length(min=4,max=50)])
    Time1 = StringField("")
    Time2 = StringField("")
    Date = DateField("Date", format='%d/%m/%Y')
    Place = StringField("Place", [validators.Length(min=1,max=50)])
    Betting_amount = IntegerField("Entry Amount($)")


@app.route('/create',methods=["GET","POST"])
def create():
    form=CreateTournament(request.form)
    if request.method=="POST" and form.validate() and 'photo' in request.files:
        name = form.Tournament_Name.data
        Time1 = form.Time1.data
        Time2=form.Time2.data
        Date=form.Date.data
        Place=form.Place.data
        Betting_amount=form.Betting_amount.data
        filename=photos.save(request.files['photo'])

        #sql
        session = Session()
        session.add(Tournament(name,Time1,Time2,Date,Place,Betting_amount,filename))
        session.commit()
        session.close()



        flash("The tournament have been created! ", "success")
        return redirect(url_for('find'))
    return render_template('createtournament.html',form=form)

@app.route('/JoinTournament')
def index():
    return render_template("jointournament.html")

@app.route('/findtournament',methods=["GET","POST"])
def find():
    global list
    listlen=matchdb_retrieve()
    session['count']=x
    return render_template('findtournament.html',list=list,id=id,listlen=listlen)


if __name__=="__main__":
    app.secret_key="secret123"
    app.run(debug=True)
