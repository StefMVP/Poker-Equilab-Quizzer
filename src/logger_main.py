import logging
import logging.handlers


class MainLogger(object):
    def __init__(self):
        self.logger = self.setup_logger()

    @staticmethod
    def setup_logger():
        try:
            log_filename = 'pb.log'
            my_logger = logging.getLogger(__name__)
            formatter = logging.Formatter('%(levelname)s %(msg)s %(pathname)s:%(lineno)s %(exc_info)s %(funcName)s')
            handler = logging.handlers.RotatingFileHandler(
                log_filename, maxBytes=7000000, backupCount=5)
            handler.setFormatter(formatter)
            my_logger.addHandler(handler)
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            my_logger.addHandler(console)

            return logging.getLogger(__name__)

        except Exception as e:
            print("Exception: Failed to setup logger %s" % e)