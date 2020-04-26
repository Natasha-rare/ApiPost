from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource
import datetime
from data import db_session
from data.request import parser
from data.jobs import Jobs


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('job', 'work_size', 'collaborators', 'team_leader', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        job = session.query(Jobs).all()
        return jsonify({'job': [item.to_dict(
            only=('job', 'work_size', 'collaborators', 'team_leader', 'is_finished')) for item in job]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            team_leader=args['team_leader'],
            is_finished=args['is_finished'],
            start_date=datetime.datetime.now,
            end_date=datetime.datetime.now
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})