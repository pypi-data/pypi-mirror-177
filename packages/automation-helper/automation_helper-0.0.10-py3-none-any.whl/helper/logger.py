import logging

msg_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
second_format = logging.Formatter('%(message)s')
date_format = '%m/%d/%Y %H:%M:%S'


def _changeLoggerFormat(log_name, format_in):
    logger = logging.getLogger(log_name)
    handlers = logger.handlers
    for handler in handlers:
        handler.setFormatter(format_in)


class Logger:
    def __init__(self, name, path):
        self.name = name
        handler = logging.FileHandler(path)
        handler.setFormatter(msg_format)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
        self.logger = logger

    def info(self, the_str):
        self.logger.setLevel(logging.INFO)
        _changeLoggerFormat(self.name, msg_format)
        self.logger.info(str(the_str))

    def secondFormatInfo(self, the_str):
        self.logger.setLevel(logging.INFO)
        _changeLoggerFormat(self.name, second_format)
        self.logger.info(str(the_str))

    def warning(self, the_str):
        self.logger.setLevel(logging.WARNING)
        _changeLoggerFormat(self.name, msg_format)
        self.logger.warning(str(the_str))
        
    def exception(self, msg="Got Exception"):
        self.logger.setLevel(logging.ERROR)
        _changeLoggerFormat(self.name, msg_format)
        self.logger.exception(msg)

    def close(self):
        self.logger.handlers.clear()
