import logging
import logging.handlers

class PaLogger(object):
    def __init__(self):
        logging.basicConfig(filename = "/var/log/palos.log", level=logging.INFO)


    def info(self, msg):
        logging.info(msg)
        return msg
        

    def error(self, msg):
        logging.error(msg)
        print(msg)

    def warn(self, msg):
        logging.warn(msg)
        print(msg)
        
        
