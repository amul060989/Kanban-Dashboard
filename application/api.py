from dataclasses import field
from flask_restful import fields, reqparse, Resource, marshal_with
from matplotlib.style import use
from application.database import db
from application.models import Tasks
from application.validation import NotFoundError,FieldNotPresentError

output_fields = {"summary":fields.String,
"description":fields.String,"status":fields.String,"id" :fields.Integer}

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('summary')
create_user_parser.add_argument('status')
create_user_parser.add_argument('description')
create_user_parser.add_argument('id')
class TaskAPI(Resource):

    @marshal_with(output_fields)
    def get(self,task_id):        
        task = db.session.query(Tasks).filter(Tasks.id == int(task_id)).first()

        if task:
            return task,200
        else:
            raise NotFoundError(status_code=404, error_message="Task does not exist.")

    @marshal_with(output_fields)
    def post(self):
        args = create_user_parser.parse_args()
        summary = args.get("summary",None)
        description = args.get("description",None)
        status = args.get("status",None)

        if summary is None or summary == '':
            raise FieldNotPresentError(status_code=400, error_code='NF101',error_message='summary cannot be blank')

        elif status is None or status == '' or status not in ['blocked','pending','progress','completed']:
            if status is None:
                raise FieldNotPresentError(status_code=400, error_code='NF102',error_message='status cannot be blank')
            else:
                raise FieldNotPresentError(status_code=400, error_code='NF102',error_message='status need to be from list')
        
        new_task = Tasks(summary=summary, status = status, description=description)
        db.session.add(new_task)
        db.session.commit()

        return new_task, 201
    
    @marshal_with(output_fields)
    def put(self,task_id):
        args = create_user_parser.parse_args()
        summary = args.get("summary",None)
        description = args.get("description",None)
        status = args.get("status",None)

        task = db.session.query(Tasks).filter((Tasks.id == int(task_id))).first()

        if task is None:
            raise NotFoundError(status_code=404, error_message="Task does not exist.")

        if summary is not None and status is None and description is None:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({"summary":summary})
            db.session.commit()
        elif summary is None and status is not None and description is None and status in ['blocked','pending','progress','completed']:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({"status":status})
            db.session.commit()
        elif summary is None and status is None and description is not None:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({"description":description})
            db.session.commit()
        elif summary is not None and status is not None and description is not None and status in ['blocked','pending','progress','completed']:
           db.session.query(Tasks).filter(Tasks.id == task_id).update({"summary":summary, 'description':description, 'status':status})
           db.session.commit()
        elif summary is None and status is not None and description is not None and status in ['blocked','pending','progress','completed']:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({'description':description, 'status':status})
            db.session.commit()
        elif summary is not None and status is None and description is not None:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({'summary':summary, 'description':description})
            db.session.commit()
        elif summary is not None and status is not None and description is None and status in ['blocked','pending','progress','completed']:
            db.session.query(Tasks).filter(Tasks.id == task_id).update({'summary':summary, 'status':status})
            db.session.commit()
        else:
            raise FieldNotPresentError(status_code=400, error_code='NF103',error_message='Wrong update performed.')
        
        updated_task = db.session.query(Tasks).filter((Tasks.id == int(task_id))).first() 
        
        return(updated_task,201)

    @marshal_with(output_fields)
    def delete(self,task_id):
        task = db.session.query(Tasks).filter(Tasks.id == int(task_id)).first()
        
        if task is None:
            raise NotFoundError(status_code=404, error_message="Task does not exist.")

        db.session.delete(task)
        db.session.commit()

        return task,200




    