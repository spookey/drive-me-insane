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
    config = _read_json(configfile)

    if config is not None:
        try:
            return config[key]
        except KeyError as e:
            logger.info('requested key does not exist: %s' %(e))
    else:
        logger.error('config file not found: %s' %(filename))
        print('config file not found: %s' %(filename))
        exit(0)

def _read_json(filename):
    if path.exists(filename):
        with open(filename, 'rb') as f:
            try:
                return json.loads(f.read().decode('utf-8'))
            except Exception as e:
                logger.error('could not read from json: %s' %(e))
    else:
        logger.error('json file not found: %s' %(filename))

def makeconf(inputdict):
    configfile = path.join(basedir, 'config.json')
    _write_json(configfile, inputdict)

def _write_json(filename, data):
    with open(filename, 'w') as f:
        try:
            f.write(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True))
        except Exception as e:
            logger.warning('could not write to json:', e)

# Edit here
test_message = 'Fire, exclamation mark, fire, exclamation mark, help me, exclamation mark. 123 Cavendon Road. Looking forward to hearing from you.\nYours truly, Maurice Moss.'

settings = {
    'email_sender': 'Maurice Moss <mossfromIT@example.com>',
    'email_subject': 'Fire!',
    'email_footer': 'your ad here\nhttp://www.example.com/',
    'email_defaulttopic': 'Warning',

    'smtp_user': 'root',
    'smtp_port': '587',
    'smtp_use_ssl': True, # uses startSSL or plain as fallback, if false
    'smtp_server': 'localhost',
    'smtp_password': '',
}

if __name__ == '__main__':
    makeconf(settings)
