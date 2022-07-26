import random
import time
import datetime

from sqlalchemy.orm import sessionmaker

import db


def random_date(timeframe, nof_entries):
    """
    Yields a generator object of unique timestamps distributed over the timeframe
    :param timeframe: range of time for datapoints with current time as the end points
    :param nof_entries: the number datapoints desired
    :return: None
    """

    current_time = datetime.datetime.utcnow()
    time_stamps = []
    # stops infinite loop by limiting nof_entries to number of available seconds in the timeframe
    if nof_entries > timeframe * 60:
        nof_entries = timeframe * 60

    while nof_entries > 0:
        timestamp = current_time - datetime.timedelta(seconds=random.randrange(timeframe*60))
        unix_time = round(time.mktime(timestamp.timetuple()))

        if unix_time not in time_stamps:
            time_stamps.append(unix_time)
            yield unix_time
            nof_entries -= 1


def generate_data(timeframe, num_datapoints):
    """
    Creates a json like set of data containing a timestamp, cpu_load and concurrency.
    The timestamps are randomly distributed over the timeframe and are unique.
    cpu_load is a random float between 0 and 100, concurrency is a random integer between 0 and 5000000

    :param timeframe: range of time in minutes for datapoints with current time as the end points
    :param num_datapoints: the number datapoints desired
    :return metrics_data: a json like data structure containing the metrics data
    """

    metrics_data = []
    timestamps = [timestamp for timestamp in random_date(timeframe, num_datapoints)]
    timestamps.sort()

    for timestamp in timestamps:
        new_entry = {"timestamp": timestamp,
                     "cpu_load": random.uniform(0, 100),
                     "concurrency": random.randint(0, 500000)
                     }
        metrics_data.append(new_entry)

    return metrics_data


def insert_data(metrics_data):
    """
    Uses an sqlalchemy session to insert the data using the db model
    :param metrics_data: json like data to be ingested into the database
    :return: None
    """
    # new session
    Session = sessionmaker(bind=db.engine)
    session = Session()

    # add the data
    for entry in metrics_data:
        timestamp = entry["timestamp"]
        cpu_load = entry["cpu_load"]
        concurrency = entry["concurrency"]
        tr = db.Metrics(timestamp, cpu_load, concurrency)
        session.add(tr)

    # commit data
    session.commit()


def main():
    # get data to be ingested
    metrics_data = generate_data(5, 100)
    # insert data into the database
    insert_data(metrics_data)


main()
