import logging
import os
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# If log directory does not exist, create one
current_d = os.getcwd()
print(current_d)
if not os.path.exists(os.path.join(current_d, 'log')):
    os.makedirs(os.path.join(current_d, 'log'))


class LoggerSetup:
    def __init__(self, name, log_file, level):
        self.name = name
        self.log_file = log_file
        self.level = level

# def setup_logger(name, log_file, level=logging.INFO):
    def setup_logger(self):
        """Function setup as many loggers as you want"""

        handler = logging.FileHandler(self.log_file, mode='w')
        handler.setFormatter(formatter)

        logger_object = logging.getLogger(self.name)
        if self.level is None:
            logger_object.setLevel(logging.INFO)
        elif self.level is 0:
            logger_object.setLevel(logging.DEBUG)
        elif self.level is 1:
            logger_object.setLevel(logging.INFO)
        elif self.level is 2:
            logger_object.setLevel(logging.WARNING)
        elif self.level is 3:
            logger_object.setLevel(logging.ERROR)
        elif self.level is 4:
            logger_object.setLevel(logging.CRITICAL)
        else:
            print('Please define correct one of the Debug Levels:\n'
                  '0: DEBUG\n'
                  '1: INFO\n'
                  '2: WARNING\n'
                  '3: ERROR\n'
                  '4: CRITICAL')

        logger_object.addHandler(handler)

        return logger_object
