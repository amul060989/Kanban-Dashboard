from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import Tasks, Users
from flask import url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from application.database import db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/login/success", methods=["GET", "POST"])
def login_success():
    if request.method == "POST":
        try:
            f_username = request.form['email']
            if f_username == '':
                f_username = None
            
            f_password = request.form['password']
            if f_password == '':
                f_password = None

            
            if f_username is not None:
                checkPassword = db.session.query(Users).filter(Users.username == f_username).first()
    
                if checkPassword is None:
                   return render_template("user_does_not_exist.html") 
                else:
                    if checkPassword.password == f_password:
                        return redirect(url_for("kanban_home_page"))
                    else:
                        return render_template("login_error.html")
            
            else:
                return render_template("user_does_not_exist.html")

        
        except:
            return render_template("blankLogin_error.html")



@app.route("/dashboard", methods=["GET", "POST"])
def kanban_home_page():
    blocked_tasks = Tasks.query.filter(Tasks.status == 'blocked')
    pending_tasks = Tasks.query.filter(Tasks.status == 'pending')
    progress_tasks = Tasks.query.filter(Tasks.status == 'progress')
    closed_tasks = Tasks.query.filter(Tasks.status == 'completed')
    return render_template("homepage.html",blocked_tasks = blocked_tasks, pending_tasks = pending_tasks, progress_tasks = progress_tasks, closed_tasks = closed_tasks)

@app.route("/new_ticket",methods=["GET", "POST"])
def new_ticket_page():
    if request.method == 'GET':
        return render_template("new_ticket.html")

@app.route("/new_ticket/success",methods=["POST"])
def success_create():
    if request.method == "POST":
        try:
            f_summary = request.form['summary']
            if f_summary == '':
                f_summary = None
            f_description = request.form['desc']
            f_status = request.form['status'].lower()

            new_task = Tasks(summary=f_summary,description=f_description, status=f_status)
            db = SQLAlchemy()
            db.session.add(new_task)
            db.session.commit()
        except:
            return render_template("error.html")

        return redirect(url_for("kanban_home_page"))

@app.route("/details/<int:task_id>",methods=["GET","POST"])
def details(task_id):
    task_detail = Tasks.query.filter(Tasks.id == task_id).all()
    return render_template("task_details.html",detail = task_detail)

@app.route("/delete/<int:task_id>",methods=["GET","POST"])
def delete_tasks(task_id):
   db = SQLAlchemy()
   db.session.query(Tasks).filter(Tasks.id == task_id).delete()
   db.session.commit()
   return redirect(url_for("kanban_home_page"))

@app.route("/update/<int:task_id>",methods=["GET","POST"])
def edit_tasks(task_id):
    edit_task = Tasks.query.filter(Tasks.id == task_id).all()
    return render_template("edit_task.html", edit_tasks = edit_task)

@app.route("/update/success/<int:task_id>",methods=["GET","POST"])
def update_task(task_id):
    if request.method == "POST":
        try:
            f_summary = request.form['summary']
            if f_summary == '':
                f_summary = None
                
            db = SQLAlchemy()
            db.session.query(Tasks).filter(Tasks.id == task_id).update({"summary":request.form.get('summary'), 'description':request.form.get('desc'), 'status':request.form.get('status').lower()})
            db.session.commit()

        except:
            return render_template("error.html")

        return redirect(url_for("kanban_home_page"))

@app.route("/new_registration")
def new_registration():
    return render_template("new_registration.html")

@app.route("/new_registration/success",methods=["GET","POST"])
def registration_success():
    if request.method == "POST":
        # print("inside post---------->")
        try:
            f_username = request.form['username']

            if f_username == '':
                f_username = None
            f_password = request.form['password']
            if f_password == '':
                f_password = None
            first_name = request.form['first_name']
            if first_name == '':
                first_name = None
            last_name = request.form['last_name']

            # print("Query Start")
            checkUsernameAvailbility = db.session.query(Users).filter(Users.username == f_username).first()

            if checkUsernameAvailbility is not None:
                return render_template("registration_error.html")
            else:
                new_user = Users(username=f_username,password=f_password, f_name=first_name, l_name=last_name)
                db.session.add(new_user)
                db.session.commit()
        except:
            return render_template("registration_error.html")
        
        return redirect(url_for("kanban_home_page"))

@app.route("/summary",methods=["GET","POST"])
def task_summary():

    blocked_tasks = db.session.query(Tasks).filter(Tasks.status == "blocked").count()
    pending_tasks = db.session.query(Tasks).filter(Tasks.status == "pending").count()
    progress_tasks = db.session.query(Tasks).filter(Tasks.status == "progress").count()
    closed_tasks = db.session.query(Tasks).filter(Tasks.status == "completed").count()
    
    print(blocked_tasks)
    left = [1, 2, 3, 4]
    height = [blocked_tasks,pending_tasks,progress_tasks,closed_tasks]

    tick_label = ['Blocked', 'Pending', 'Progress', 'Closed']

    plt.bar(left,height,tick_label = tick_label,width = 0.5, color = ['red', 'orange','yellow','green'])

    
    plt.xlabel('Tasks')
    plt.title('Task Trends')

    plt.savefig("./static/image/trend.png")

    return render_template("summary.html",image="./static/image/trend.png")





