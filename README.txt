Metrics API and Ingestion Layer
-------------------------------------
This README is a guide for use of the following components:
db.py - used to build the database and contains the database model.
ingestion_layer.py - used to generate random timeseries metrics data for the last 5 minutes which is then added to the
                     database.
metrics_api.py - a Flask based API used to expose the metrics data held in the database.


REQUIREMENTS:
Before running please install the required packages using the following command:

pip install -r requirements.txt
--------------------------------------

Building the database using db.py

The database layer employs sqlite as the database type and sqlalchemy as the ORM

The database model contains one table called Metrics. The class is shown below for reference

example:

class Metrics (base):

    __tablename__ = "Metrics"

    timestamp = Column(Integer, primary_key=True)
    cpu_load = Column(Float)
    concurrency = Column(Integer)

    def __init__(self, timestamp, cpu_load, concurrency):
        self.timestamp = timestamp
        self.cpu_load = cpu_load
        self.concurrency = concurrency


To build the database simply run db.py

----------------------------------------]
Running the INGESTION_LAYER - ingestion_layer.py:

Simply running ingestion_layer.py will result in the creation of 100 unique new records with unix timestamp data
randomly distributed over the last 5 minutes; cpu_load is a randomly generated float between 0 and 100;
concurrency is a random integer between 0 and 50000

WARNING: at present the ingestion layer can only be run every 5 minutes. Running the ingestion layer more frequently
will result in an error.

functions:
main() contains the flow


def insert_data(metrics_data):
    """
    Uses an sqlalchemy session to insert the data using the db model
    :param metrics_data: json like data to be ingested into the database
    :return: None
...

def generate_data(timeframe, num_datapoints):
    """
    Creates a json like set of data containing a timestamp, cpu_load and concurrency.
    The timestamps are randomly distributed over the timeframe and are unique.
    cpu_load is a random float between 0 and 100, concurrency is a random integer between 0 and 5000000

    :param timeframe: range of time in minutes for datapoints with current time as the end points
    :param num_datapoints: the number datapoints desired
    :return metrics_data: a json like data structure containing the metrics data
    """
...

def random_date(timeframe, nof_entries):
    """
    Yields a generator object of unique timestamps distributed over the timeframe
    :param timeframe: range of time for datapoints with current time as the end points
    :param nof_entries: the number datapoints desired
    :return: None
    """

------------------------------------------------------------
Using the METRICS API - metrics_api.py

The Metrics API exposed the database created earlier in this document. It provides methods that can be used to access
that data in a variety of ways. These methods are intended for use in front end development.

The metrics api is in development. In order to use the flask application whilst in development please run the following
commands in your terminal

> ./sky_interview % export FLASK_APP=metrics_api.py
> ./sky_interview % export FLASK_ENV=development
> ./sky_interview % flask run

This will run flask and provide you with an address from which you can investigate.

The methods currently available are:

- add_metric(): used to insert a cpu_load/concurrency pair. The timestamp can be provided else is automatically
                generated.
- get_max_cpu_load(): returns record with the maximum cpu_load value
- get_min_cpu_load(): returns record with the minimum cpu_load value
- get_metrics_on_date(date): takes a date in the form "yyyy-mm-dd" and provides all data from that day else throws 404
- get_metrics: returns all current records.

Future methods:
To be complete

Technical debt:
The developer wishes in future to migrate to using the native flask-sqlalchemy over the current use of the standalone
sqlalchemy. This is to make use of the built-in functions provided by it that specifically aid in an API build


