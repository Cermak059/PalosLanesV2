import logging
import logging.handlers

class PaLogger(object):
    def __init__(self, name, filepath):
        self.name = name
        logging.basicConfig(filename = filepath, level=logging.INFO)
        self.logger = logging.getLogger(name)
        self.handler = logging.handlers.RotatingFileHandler(filepath, maxBytes=10000000, backupCount=3)
        self.logger.addHandler(self.handler)


    def info(self, msg):
        self.logger.info(msg)
        print(msg)
        

    def error(self, msg):
        self.logger.error(msg)
        print(msg)

    def warn(self, msg):
        self.logger.warn(msg)
        print(msg)
        
        
