import pendulum


def to_millis(dt):
    return dt.timestamp() * 1000


def get_cur_week0():
    return pendulum.now().start_of('week')


def get_cur_week1():
    return pendulum.now().end_of('week')


def get_to_minute(dt=pendulum.now()):
    return dt.strftime("%Y%m%d_%H%M")


def get_to_day(dt=pendulum.now()):
    return dt.strftime("%Y%m%d")


def get_cur_csv_id():
    return pendulum.now().strftime("%Y%m%d_%H%M")
