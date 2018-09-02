''' bootstrap.py '''
import os

def bootstrap(db_name, logger):
    '''
    Bootstrap the application / db / etc
    '''
    db_file = os.path.abspath(db_name)

    if os.path.isfile(db_file) is False:
        from sorter.lib.first_run import init
        logger.info('First run, initializing application')
        init(db_file)

    return db_file
