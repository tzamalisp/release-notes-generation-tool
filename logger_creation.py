import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


class LoggerSetup:
    def __init__(self, name, log_file, level):
        self.name = name
        self.log_file = log_file
        self.level = level

# def setup_logger(name, log_file, level=logging.INFO):
    def setup_logger(self):
        """Function setup as many loggers as you want"""

        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(formatter)

        logger_object = logging.getLogger(self.name)
        logger_object.setLevel(self.level)
        logger_object.addHandler(handler)

        return logger_object
