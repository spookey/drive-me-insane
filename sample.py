# -.- coding: utf-8 -.-

from util import logger, test_message
from aspsms import send_aspsms
from mail import send_mail

if __name__ == '__main__':

    logger.info('Sending new test mail')
    send_mail(['mail@example.com'], test_message, subject='test')

    logger.info('Sending new test aspsms')
    send_aspsms(['00991234567890'], test_message)

    logger.info('Sending new mail with all parameters')
    send_mail(
        ['one@example.com', 'two@example.com'],
        'Have fun with the readme!',
        subject='mail to many recipients',
        subjecttag='Information',
        subjectdate=True,
        cc=['three@example.com', 'four@example.com'],
        bcc=['five@example.com'],
        sender='Sample User <me@example.com>',
        footer='Fnord Industries 2000\nSky\'s-the-limit-lane 23\n23425 Fnord',
        files=['README.markdown']
        )

    logger.info('Sending new aspsms with all parameters')
    send_aspsms(
        ['00991234567890', '00119876543210'],
        'This is a very important message',
        originator='SampleUser',
        flashing=True,
        maxchars=320
        )

