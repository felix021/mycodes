import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s][%(asctime)s] %(message)s')

logging.debug('Hello %s, %s!', 'World', 'Congratulations')
logging.info('Hello %s, %s!', 'World', 'Congratulations')
logging.warn('Hello %s, %s!', 'World', 'Congratulations')
logging.error('Hello %s, %s!', 'World', 'Congratulations')
logging.fatal('Hello %s, %s!', 'World', 'Congratulations')
