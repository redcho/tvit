from yaml import load, FullLoader
from helper.bt_logging import get_logger


class Configuration(object):
    l = get_logger(__name__)

    @classmethod
    def get_conf(self, filename):
        try:
            f = open(filename, 'r')
            return load(f, Loader=FullLoader)
        except Exception as e:
            self.l.error(f"Failed to read file {filename}")
            self.l.error(e)
            raise
