from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import db

Session = sessionmaker(bind=db.engine)
session = Session()

#data = session.query(db.metrics).all()
data = session.query(db.Metrics, func.max(db.Metrics.cpu_load)).all()

for s in data:
    print(s[0].timestamp, s[0])
