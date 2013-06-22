# -.- coding: utf-8 -.-

from util import logger, getconf
from mail import send_mail

if __name__ == '__main__':

    logger.info('Sending new test mail')
    send_mail(['mail@example.com'], getconf('test_message'), subject='test')
