from flask import Flask, session, request, redirect, render_template, url_for, jsonify, send_file
from flask_caching import Cache
from flask_session import Session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery_systems import make_celery
import csv, time, redis, json
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
from celery import Celery
from functools import wraps
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from celery.schedules import crontab
import cache_config
import os
from weasyprint import HTML
import uuid
from flask_login import *


#app
app = Flask(__name__)



CORS(app, supports_credentials=True)


basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SECRET_KEY']='1234dfghjk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'everything.db')
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()
app.secret_key = '1234dfghjk'
app.app_context().push()

#login
login_manager = LoginManager()
login_manager.init_app(app)

#api
api = Api(app)
app.app_context().push()

#celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='redis://localhost:6379/2',
    CELERY_TIMEZONE= "Asia/Calcutta",
    CELERY_ENABLE_UTC = False
)

celery = make_celery(app)
app.app_context().push()

#Caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 20

app.config.from_object(
cache_config
)
 
cache = Cache(app)
app.app_context().push()





@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour = 10, minute='30'),
        dailyreminder.s(),
        name='Daily Reminders'
    )
    sender.add_periodic_task(
        crontab(hour = 10, minute='30', day_of_month='1'),
        monthlyreport.s(),
        name='Monthly Report'
    )
    





class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique = True)
    password = db.Column(db.String, nullable=False)



class ListModel(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(100), nullable=False, unique = True)
    user = db.Column(db.Integer, nullable=False)
    ldescription = db.Column(db.String, nullable=True)

class CardModel(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(100), nullable=False)
    lid = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, nullable=False)
    cdescription = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable = False)
    creation_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deadline_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)

db.create_all()

#Daily Reminders
@celery.task
def dailyreminder():
    lpendingc = []
    dpendingl = {}
    users = UserModel.query.all()
    for user in users:
        lists = ListModel.query.filter_by(user = user.id).all()
        for list in lists:
            cards = CardModel.query.filter_by(lid = list.lid, completed = 0 ).all()
            for card in cards:
                lpendingc.append(card.cname)
            dpendingl[list.lname]= lpendingc
            lpendingc = []
        with open ("dailyreminder.html") as file_:
            template = Template(file_.read())
            message =  template.render(data=dpendingl)
        msg = MIMEMultipart()
        msg [ "From"] = "jankanban100@gmail.com"
        msg ["To"] = user.name
        msg ["Subject"] = "JanKanBan Report for Today"
        msg.attach (MIMEText (message, "html"))
        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login ("jankanban100@gmail.com", "jehvayerievdjdpi")
        s.send_message(msg)
        s.quit()
        print("sent")
        dpendingl = {}

    return 

#Monthly Report
@celery.task
def monthlyreport():
    lofc = []
    dofl = {}
    users = UserModel.query.all()
    for user in users:
        lists = ListModel.query.filter_by(user = user.id).all()
        for list in lists:
            cards = CardModel.query.filter_by(lid = list.lid).all()
            dofl[list.lname] = []
            for card in cards:
                lofc.append(card.cname)
                lofc.append(str(card.creation_date)[0:str(card.creation_date).rindex(':')]) 
                if(card.completed):
                    lofc.append(str(card.completion_date)[0:str(card.completion_date).rindex(':')])
                else:
                    lofc.append("PENDING") 
                lofc.append((str(card.deadline_date)[0:str(card.deadline_date).rindex(':')]))
                if(not card.completed):
                    lofc.append(str(datetime.now() - card.creation_date)[0:str(datetime.now() - card.creation_date).rindex(':')])
                else:
                    lofc.append("COMPLETED")
                if(card.completed):
                    lofc.append(str(card.completion_date - card.creation_date)[0:str(card.completion_date - card.creation_date).rindex(':')])
                else:
                    lofc.append("PENDING")
                
                dofl[list.lname].append(lofc)
                lofc = []
                

        with open ("report-template.html") as file_:
            template = Template(file_.read())
            message =  template.render(data=dofl)

        html = HTML (string=message)
        file_name = str(uuid.uuid4()) + ".pdf"
        html.write_pdf(target=file_name)

        msg = MIMEMultipart()
        msg [ "From"] = "jankanban100@gmail.com"
        msg ["To"] = user.name
        msg ["Subject"] = "JanKanBan Report for This Month"
        msg.attach (MIMEText (message, "html"))

        with open(file_name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload (attachment.read())
        encoders.encode_base64 (part)
        part.add_header(
            "Content-Disposition", f"attachment; filename= {file_name}",
        )
        msg.attach(part)
        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        s.login ("jankanban100@gmail.com", "jehvayerievdjdpi")
        s.send_message(msg)
        s.quit()
        print("sent")
        dofl = {}
        os.remove(file_name)
        print("deleted")

    return 



user_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username is required", required=True)
user_post_args.add_argument("password", type=str, help="Password", required=True)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class Login(Resource):
    def get(self):
        a = {"a": "loginpage"}
        return jsonify(a)

    @marshal_with(user_resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        u = UserModel.query.filter_by(name = args["username"], password = args["password"]).all()
        if(u != []):
            login_user(u[0])
            return u
        if(u == []):
            return jsonify({"user":"registerpage"})


api.add_resource(Login, "/login")




class Register(Resource):
    def get(self):
        a = {"a": "registerpage"}                                                                                       
        return jsonify(a)


    @marshal_with(user_resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        if(args["username"].strip() == '' or args["password"].strip()== ''):
            return jsonify({"error:incomplete credentials"})
        u = UserModel.query.filter_by(name = args["username"]).all()
        if(u != []):
            return jsonify({"id": 0,"name": None,"password": None})
        if(u == []):
            user = UserModel(name=args['username'].strip(), password=args['password'].strip())
            db.session.add(user)
            db.session.commit()
            u = UserModel.query.filter_by(name = args["username"], password = args["password"]).first()
            return u
            

api.add_resource(Register, "/register")




class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return jsonify({"status":"logged out"})


api.add_resource(Logout, "/logout")


list_resource_fields = {
    'lid': fields.Integer,
    'lname': fields.String,
    'user': fields.Integer,
    'ldescription': fields.String
}
list_put_args = reqparse.RequestParser()
list_put_args.add_argument("name", type=str, help="Name of the list is required", required=True)
list_put_args.add_argument("description", type=str, help="Description", required=True)


list_patch_args = reqparse.RequestParser()
list_patch_args.add_argument("old_name", type=str, help="Old name of the list is required", required=True)
list_patch_args.add_argument("new_name", type=str, help="New name of the list is required", required=True)
list_patch_args.add_argument("new_description", type=str, help="Description")


list_del_args = reqparse.RequestParser()
list_del_args.add_argument("id", type=str, help="ID of the list is required", required=True)



class List(Resource):
    
    @login_required
    @marshal_with(list_resource_fields)
    def put(self,user_id):
        args = list_put_args.parse_args()
        list = ListModel(lname=args['name'], user=user_id, ldescription=args['description'])
        db.session.add(list)
        db.session.commit()
        return list, 201

    @login_required
    @marshal_with(list_resource_fields)
    def get(self, user_id):
        list = ListModel.query.filter_by(user = user_id).all()
        return list, 201

    @login_required
    @marshal_with(list_resource_fields)
    def patch(self, user_id):
        args = list_patch_args.parse_args()
        u = ListModel.query.filter_by(user = user_id, lname = args["old_name"]).first()
        if(args["new_name"]):
            u.lname = args["new_name"]
        if args["new_description"]:
            u.ldescription = args["new_description"]
        db.session.commit()
        return u

    @login_required
    @marshal_with(list_resource_fields)
    def delete(self,user_id):
        args = list_del_args.parse_args()
        list = ListModel.query.filter_by(user = user_id, lid = args["id"]).first()
        db.session.delete(list)
        db.session.commit()
        cards = CardModel.query.filter_by(user = user_id, lid = args["id"]).all()
        for i in cards:
            db.session.delete(i)
            db.session.commit()
        return 201


api.add_resource(List, "/<int:user_id>")


card_resource_fields = {
    'cid': fields.Integer,
    'cname': fields.String,
    'lid': fields.Integer,
    'user': fields.Integer,
    'cdescription': fields.String,
    'completed': fields.Boolean,
    'creation_date': fields.String,
    'deadline_date': fields.String,
    'completion_date': fields.String
}

card_put_args = reqparse.RequestParser()
card_put_args.add_argument("name", type=str, help="Name of the card is required", required=True)
card_put_args.add_argument("description", type=str, help="Description", required=True)
card_put_args.add_argument("deadline", type=str, help="Deadline is required", required=True)

card_del_args = reqparse.RequestParser()
card_del_args.add_argument("id", type=str, help="ID of the list is required", required=True)

card_patch_args = reqparse.RequestParser()
card_patch_args.add_argument("id", type=str, help="ID of the card is required", required = True)
card_patch_args.add_argument("new_name", type=str, help="New name of the card")
card_patch_args.add_argument("new_description", type=str, help="Description")
card_patch_args.add_argument("new_list_location", type=str, help="New Location")
card_patch_args.add_argument("new_card_deadline", type=str, help="New Deadline")




class Card(Resource):

    @login_required
    @marshal_with(card_resource_fields)
    def get(self, user_id, list_id):
        cards = CardModel.query.filter_by(user = user_id, lid = list_id).all()
        return cards, 201


    @login_required
    @marshal_with(card_resource_fields)
    def put(self,user_id, list_id):
        crtime = datetime.now()
        args = card_put_args.parse_args()
        deadl = datetime.strptime(args["deadline"], '%Y-%m-%d')
        if(deadl<crtime):
            return 
        card = CardModel(cname=args['name'], lid = list_id, user=user_id, cdescription=args['description'], completed = 0, creation_date= crtime )
        deadll = (datetime.strptime(args["deadline"], '%Y-%m-%d') +timedelta(hours=23, minutes=59) )
        card.deadline_date = deadll
        db.session.add(card)
        db.session.commit()
        return card, 201
    
    @login_required
    @marshal_with(card_resource_fields)
    def delete(self,user_id, list_id):
        args = card_del_args.parse_args()
        card = CardModel.query.filter_by(cid = args["id"], user = user_id).first()
        db.session.delete(card)
        db.session.commit()
        return 201

    
    @login_required
    @marshal_with(card_resource_fields)
    def patch(self, user_id, list_id):
        args = card_patch_args.parse_args()
        card = CardModel.query.filter_by(user = user_id, cid = args["id"]).first()
        if args["new_name"]:
            card.cname = args["new_name"]
        if args["new_description"]:
            card.cdescription = args["new_description"]
        if args["new_list_location"]:
            new_location_id = ListModel.query.filter_by(lname=args['new_list_location'], user=user_id).first().lid
            card.lid = new_location_id
        if args["new_card_deadline"]:
            deadll = (datetime.strptime(args["new_card_deadline"], '%Y-%m-%d') +timedelta(hours=23, minutes=59) )
            card.deadline_date = deadll
        db.session.commit()
        return card


api.add_resource(Card, "/<int:user_id>/<int:list_id>")

class CardPending(Resource):
    @login_required
    @marshal_with(card_resource_fields)
    def get(self, user_id, list_id, card_id):
        card = CardModel.query.filter_by(cid = card_id, lid = list_id).first()
        card.completed = 1
        card.completion_date = datetime.now()
        db.session.commit()
        return card, 201

api.add_resource(CardPending, "/<int:user_id>/<int:list_id>/<int:card_id>")

argu = reqparse.RequestParser()
argu.add_argument("num", type = int, required = True)




class Summary(Resource):
    @cache.cached(timeout=30)
    @login_required
    def get(self, user_id):
        u = ListModel.query.filter_by(user = user_id).all()
        p = {}
        lop = []
        noc = 0
        noic = 0
        for i in u:
            
            card = CardModel.query.filter_by(lid = i.lid).all()
            p["lid"] = i.lid
            p["lname"] = i.lname
            for j in card:
                if(j.completed):
                    noc = noc + 1
                else:
                    noic = noic + 1
            p["completed"] = noc
            p["incomplete"] = noic
            lop.append(p)
            noc = 0
            noic = 0
            p = {}    


        return(jsonify(lop))

api.add_resource(Summary, "/summary/<int:user_id>")


class CompDate(Resource):
    @cache.cached(timeout=30)
    @login_required
    def get(self, user_id):
        u = ListModel.query.filter_by(user = user_id).all()
        p = {}
        lop = []

        for i in u:
           
            cards = CardModel.query.filter_by(lid = i.lid).all()
            p[i.lname] = []
            for j in cards:
                if(j.completed):
                  print(j.completion_date - j.creation_date)
                  p[i.lname].append([i.lname,j.cname,j.completion_date, str(j.completion_date - j.creation_date)])  
            if(p[i.lname] == []):
                del p[i.lname]
        return(jsonify(p))

api.add_resource(CompDate, "/compdate/<int:user_id>")


@celery.task()
def ltocsv(useri):
    listll = ListModel.query.filter_by(user = useri).all()
    tt = []
    tq = {}
    for i in listll:
        tq['lid'] = i.lid
        tq['lname'] = i.lname
        tq['user'] = i.user
        tq['ldescription'] = i.ldescription
        tt.append(tq)
        tq = {}    
    with open('dump.csv', 'w', newline='') as f:
        out = csv.writer(f)
        out.writerow(['lid', 'lname', 'user', 'ldescription'])
        print(tt)
        for item in tt:
            out.writerow([item['lid'], item['lname'], item['user'], item['ldescription']])
        f.close()
        print("written")
        
    return 

class ListExport(Resource):
    def get(self,user_id):
        t = ltocsv.delay(user_id)
        while(not t.ready()):
            time.sleep(1)
        return(send_file("dump.csv", as_attachment= True))


api.add_resource(ListExport, "/listexport/<int:user_id>")


@celery.task()
def ctocsv(id):
    listll = CardModel.query.filter_by(user = id).all()
    tt = []
    tq = {}
    for i in listll:
        tq['cid'] = i.cid
        tq['cname'] = i.cname
        tq['lid'] = i.lid
        tq['user'] = i.user
        tq['cdescription'] = i.cdescription
        tq['completed'] = i.completed
        tq['creation_date'] = i.creation_date
        tq['deadline_date'] = i.deadline_date
        tq['completion_date'] = i.completion_date
        tt.append(tq)
        tq = {}
    
    with open('dump.csv', 'w', newline='') as f:
        out = csv.writer(f)
        out.writerow( ['cid','cname','lid','user','cdescription','completed','creation_date','deadline_date','completion_date'] )
        print(tt)
        for item in tt:
            out.writerow( [item['cid'], item['cname'], item['lid'], item['user'], item['cdescription'],item['completed'],item['creation_date'], item['deadline_date'],item['completion_date']])
        f.close()
        print("written")
        
    return 



class CardExport(Resource):
   
    def get(self,user_id):
        t = ctocsv.delay(user_id)
        while(not t.ready()):
            time.sleep(1)
        return (send_file("dump.csv", as_attachment= True))


api.add_resource(CardExport, "/cardexport/<int:user_id>")


class ForgotPassword(Resource):
    def get(self,user_email):
        u = UserModel.query.filter_by(name = user_email).all()
        if(u != []):
            with open ("Forgotpassword.html") as file_:
                template = Template(file_.read())
                message =  template.render(password = u[0].password)
            msg = MIMEMultipart()
            msg [ "From"] = "jankanban100@gmail.com"
            msg ["To"] = user_email
            msg ["Subject"] = "Password Request"
            msg.attach (MIMEText (message, "html"))
            s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
            s.login ("jankanban100@gmail.com", "jehvayerievdjdpi")
            s.send_message(msg)
            s.quit()
            print("sent")
            return {"user":"The password has been sent to your email. Thank you."}

        if(u == []):
            return jsonify({"user":"user email does not exist"})

api.add_resource(ForgotPassword, "/forgotpassword/<string:user_email>")





if __name__ == "__main__":
    app.run(debug = True) 