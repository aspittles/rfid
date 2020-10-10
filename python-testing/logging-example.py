import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
logging.warning('is when this event was logged.')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


