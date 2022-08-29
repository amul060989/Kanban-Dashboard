from application.database import db

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, autoincrement=True, primary_key = True, nullable = False)
    summary = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    status = db.Column(db.String, nullable = False)