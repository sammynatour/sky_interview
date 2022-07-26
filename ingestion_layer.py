import random
import time
import datetime

from sqlalchemy.orm import sessionmaker

import db


def random_date(timeframe, nof_entries):
    """

    :param timeframe:
    :param nof_entries:
    :return:
    """

    current_time = datetime.datetime.utcnow()
    time_stamps = []
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

    :param timeframe: time
    :param num_datapoints:
    :return:
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

    :param metrics_data:
    :return:
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

print()
#TODO passargs