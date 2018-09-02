''' sorter_logger.py '''
import logging

def sorter_logger(name):
    ''' configure the logger for the sorter module '''
    logging.basicConfig(format='[%(asctime)-15s] %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger
