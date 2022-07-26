from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

# connect database
engine = create_engine('sqlite:///sqlalchemy.sql', echo=True)
# manage tables
base = declarative_base()


class Metrics (base):

    __tablename__ = "Metrics"

    timestamp = Column(Integer, primary_key=True)
    cpu_load = Column(Float)
    concurrency = Column(Integer)

    def __init__(self, timestamp, cpu_load, concurrency):
        self.timestamp = timestamp
        self.cpu_load = cpu_load
        self.concurrency = concurrency


base.metadata.create_all(engine)

