import datetime

from flask import Flask, request, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from flask import jsonify
import db

app = Flask(__name__)


@app.route('/')
def index():
    return "Home of All Metrics!"


@app.route('/metrics')
def get_metrics():
    Session = sessionmaker(bind=db.engine)
    session = Session()

    data = session.query(db.Metrics).all()
    metrics = []
    for s in data:
        metric = {"timestamp": s.timestamp,
                  "cpu_load": s.cpu_load,
                  "concurrency": s.concurrency}
        metrics.append(metric)

    return jsonify(metrics)


@app.route('/metrics/<date>')
def get_metrics_on_date(date):

    Session = sessionmaker(bind=db.engine)
    session = Session()

    split_date = [int(s) for s in date.split("-")]
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]
    dt = datetime.datetime(year, month, day)
    lowerbound = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
    upperbound = lowerbound + 24*60*60 - 1

    data = session.query(db.Metrics).filter(db.Metrics.timestamp.between(lowerbound, upperbound)).all()
    metrics = []
    for s in data:
        metric = {"timestamp": s.timestamp,
                  "cpu_load": s.cpu_load,
                  "concurrency": s.concurrency}
        metrics.append(metric)

    if len(metrics) == 0:
        abort(404)

    return jsonify(metrics)


@app.route('/max_cpu_load')
def get_max_cpu_load():
    Session = sessionmaker(bind=db.engine)
    session = Session()

    data = session.query(db.Metrics, func.max(db.Metrics.cpu_load)).all()

    metrics = []
    print(data)
    for s in data:
        metric = {"timestamp": s[0].timestamp,
                  "cpu_load": s[0].cpu_load,
                  "concurrency": s[0].concurrency}
        metrics.append(metric)

    return jsonify(metrics)


@app.route('/min_cpu_load')
def get_min_cpu_load():
    Session = sessionmaker(bind=db.engine)
    session = Session()

    data = session.query(db.Metrics, func.min(db.Metrics.cpu_load)).all()

    metrics = []
    for s in data:
        metric = {"timestamp": s[0].timestamp,
                  "cpu_load": s[0].cpu_load,
                  "concurrency": s[0].concurrency}
        metrics.append(metric)

    return jsonify(metrics)


@app.route('/metrics', methods=['POST'])
def add_metric():
    Session = sessionmaker(bind=db.engine)
    session = Session()
    if not request.json['timestamp']:
        timestamp = round(datetime.datetime.utcnow().timestamp())
    else:
        timestamp = request.json['timestamp']
    metric = db.Metrics(timestamp=timestamp,
                        cpu_load=request.json['cpu_load'],
                        concurrency=request.json['concurrency'])

    session.add(metric)
    session.commit()

    return {"timestamp": metric.timestamp, "cpu_load": metric.cpu_load, "concurrency": metric.cpu_load}
