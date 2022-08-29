from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import Tasks
from flask import url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

@app.route("/", methods=["GET", "POST"])
def kanban_home_page():
    blocked_tasks = Tasks.query.filter(Tasks.status == 'blocked')
    pending_tasks = Tasks.query.filter(Tasks.status == 'pending')
    progress_tasks = Tasks.query.filter(Tasks.status == 'progress')
    closed_tasks = Tasks.query.filter(Tasks.status == 'completed')
    return render_template("index.html",blocked_tasks = blocked_tasks, pending_tasks = pending_tasks, progress_tasks = progress_tasks, closed_tasks = closed_tasks)

@app.route("/new_ticket",methods=["GET", "POST"])
def new_ticket_page():
    if request.method == 'GET':
        print('This is test')
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

        return redirect('/')