# -.- coding: utf-8 -.-

import json
import logging
from logging.handlers import TimedRotatingFileHandler
from os import path

basedir = path.abspath(path.dirname(__file__))
configfile = path.join(basedir, 'config.json')
logfile = path.join(basedir, 'logfile.log')

filehandler = TimedRotatingFileHandler(logfile, 'H', 1, 24)
filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'))

logger = logging.getLogger('drive-me-insane')
logger.setLevel(logging.INFO)
logger.addHandler(filehandler)

def getconf(key):
    if path.exists(configfile):
        with open(configfile, 'rb') as f:
            try:
                return json.loads(f.read().decode('utf-8'))[key]
            except KeyError as e:
                logger.info('requested key does not exist: %s' %(e))
            except Exception as e:
                logger.error('could not read from json: %s' %(e))
    else:
        logger.error('config file not found: %s' %(configfile))
        print('config file not found: %s' %(configfile))
        exit(0)

def makeconf(inputdict):
    configfile = path.join(basedir, 'config.json')
    with open(configfile, 'w') as f:
        try:
            f.write(json.dumps(inputdict, ensure_ascii=False, indent=4, sort_keys=True))
        except Exception as e:
            logger.warning('could not write to json:', e)

settings = {

    'test_message': 'Fire, exclamation mark, fire, exclamation mark, help me, exclamation mark. 123 Cavendon Road. Looking forward to hearing from you.\nYours truly, Maurice Moss.',
    'email_sender': 'Maurice Moss <mossfromIT@example.com>',
    'email_subject': 'Fire!',
    'email_footer': 'your ad here\nhttp://www.example.com/',

    'smtp_user': 'root',
    'smtp_server': 'localhost',
    'smtp_password': '',
}

if __name__ == '__main__':
    makeconf(settings)
