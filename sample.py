# -.- coding: utf-8 -.-

from .util import logger, test_message
from .mail import send_mail

if __name__ == '__main__':

    logger.info('Sending new test mail')
    send_mail(['mail@example.com'], test_message, subject='test')

    logger.info('Sending new mail with all parameters')
    send_mail(
        ['one@example.com', 'two@example.com'],
        'Hello you two, I\'ve added some other recipients and the readme',
        subject='mail to many recipients',
        subjecttopic='Information',
        subjectdate=True,
        cc=['three@example.com', 'four@example.com'],
        bcc=['five@example.com'],
        sender='Sample User <me@example.com>',
        footer='Fnord Industries 2000\nSky\'s-the-limit-lane 23\n23425 Fnord',
        files=['README.md']
        )
