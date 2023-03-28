import datetime
import os



def mkdir_hour(path):

    os.makedirs(path, exist_ok=True)
    hours = range(00,24)
    for hour in hours:
        hour0 = "%02d"%hour
        os.makedirs(os.path.join(path, hour0), exist_ok=True)


if __name__ == '__main__':

    path = r"/opt/log2/"
    today = datetime.date.today() + datetime.timedelta(days=1)
    mkdir_hour(os.path.join(path,str(today)))
    tomorrow = datetime.date.today() + datetime.timedelta(days=2)
    mkdir_hour(os.path.join(path,str(tomorrow)))
    day_after_tomorrow = datetime.date.today() + datetime.timedelta(days=3)
    mkdir_hour(os.path.join(path,str(day_after_tomorrow)))
