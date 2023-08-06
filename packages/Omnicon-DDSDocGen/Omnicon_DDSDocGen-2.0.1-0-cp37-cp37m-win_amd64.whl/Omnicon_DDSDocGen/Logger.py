import logging

fh = logging.FileHandler('DocGen' + '.log', mode='w')


def parse_logging_level(verbosity: str):
    # Check if input is a string:
    if type(verbosity) != str:
        # When not a string, print warning message and choose the default INFO
        error_message: str = f"[WARNING]: Invalid input! Parameter <logging_verbosity> '{verbosity}' is: " \
                             f"{type(verbosity)}. Should be of class 'string'.\nUsing the default verbosity 'INFO'."
        print(error_message)
        return logging.INFO

    verbosity = verbosity.upper()
    if verbosity == 'CRITICAL':
        return logging.CRITICAL
    elif verbosity == 'ERROR':
        return logging.ERROR
    elif verbosity == 'WARNING':
        return logging.WARNING
    elif verbosity == 'INFO':
        return logging.INFO
    elif verbosity == 'DEBUG':
        return logging.DEBUG
    else:
        error_message = f"[WARNING]: Invalid input! Parameter <verbosity_level> is {verbosity}. Should be either " \
                        f"'CRITICAL','ERROR','WARNING','INFO' or 'DEBUG'. \nUsing the default verbosity 'INFO'."
        print(error_message)
        return logging.INFO


def init_logger(module_name, verbosity):
    # Start by setting the root logger:
    verbosity_level = parse_logging_level(verbosity)
    root_logger = logging.getLogger()
    root_logger.setLevel(verbosity_level)
    root_logger.propagate = False
    # create file handler which logs even debug messages
    # fh = logging.FileHandler('DocGen' + '.log', mode='w')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(verbosity_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the root logger
    root_logger.addHandler(ch)
    root_logger.addHandler(fh)

    # Then create the current module's logger (that will use the root logger's configuration):
    logger = logging.getLogger(module_name)
    return logger


def add_logger(module_name):
    logger = logging.getLogger(module_name)

    return logger
