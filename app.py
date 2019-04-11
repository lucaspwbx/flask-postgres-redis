from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from rq import Queue
from rq.job import Job
from worker import conn

from foo_job import job_test

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# initializing queue for connection conn
q = Queue(connection=conn)

@app.route('/')
def hello():
    #job = q.enqueue_call(func=job_test, result_ttl=5000)
    job = q.enqueue(job_test)
    return str(job.id)

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    print(job.result)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "No!", 202

if __name__ == '__main__':
    app.run()
