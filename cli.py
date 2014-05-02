# -.- coding: utf-8 -.-

from argparse import ArgumentParser
from aspsms import send_aspsms
from twitter import send_tweet
from mail import send_mail
try:
    from util import logger, sample_settings
except ImportError:
    from .util import logger, sample_settings


def mail(params):
    logger.info('cli sends mail')
    response = send_mail(params.to, params.message, subject=params.subject, subjecttag=params.subjecttag, subjectdate=params.subjectd, cc=params.cc, bcc=params.bcc, files=params.files, sender=params.sender, footer=params.footer)
    if response == True:
        parser.exit(status=0, message='success, mail sent\n')
    else:
        parser.exit(status=-1, message='fail: %s\n' %(response))

def aspsms(params):
    logger.info('cli sends aspsms')
    response = send_aspsms(params.to, params.message, originator=params.origin, flashing=params.flashing, maxchars=params.maxchars)
    if response == True:
        parser.exit(status=0, message='success, aspsms sent\n')
    else:
        parser.exit(status=-1, message='fail: %s\n' %(response))

def gsmsms(params):
    pass

def twitter(params):
    logger.info('cli sends tweet')
    response = send_tweet(params.message, mention=params.mention)
    if response == True:
        parser.exit(status=0, message='success, tweet sent\n')
    else:
        parser.exit(status=-1, message='fail: %s\n' %(response))

functions = {'mail': mail, 'aspsms': aspsms, 'gsmsms': gsmsms, 'twitter': twitter}
parser = ArgumentParser(prog='drive-me-insane', description='drive-me-insane command line interface', epilog='Willy cares', add_help=True)

def main():
    parser.add_argument('type', action='store', choices=list(functions.keys()), help='which type of message do you want to send?')
    mailgroup = parser.add_argument_group('mail', description='mail exclusive features')
    aspsmsgroup = parser.add_argument_group('aspsms', description='aspsms exclusive features')
    gsmsmsgroup = parser.add_argument_group('gsmsms', description='gsmsms exclusive features')
    twittergroup = parser.add_argument_group('twitter', description='twitter exclusive features')

    parser.add_argument('to', action='store', nargs='*', help='destination address(es) according to message type e.g.: one@example.com or space separated for multiple e.g.: one@example.com two@example.com. This behaves similar for sms e.g.: +1234567 or for multiple e.g.: +1234567 +7654321')
    parser.add_argument('message', action='store', help='"message text" (use quotes, please)')

    mailgroup.add_argument('--subject', action='store', help='message subject (use quotes, if you have whitespace in it)')
    mailgroup.add_argument('--subjecttag', action='store', help='prefix the subject with a tag in square brackets')
    mailgroup.add_argument('--subjectd', action='store_true', help='append current date to message subject')
    mailgroup.add_argument('--cc', action='store', nargs='*', default='', help='cc this message')
    mailgroup.add_argument('--bcc', action='store', nargs='*', default='', help='bcc this message')
    mailgroup.add_argument('--files', action='store', nargs='*', default='', help='append files')
    mailgroup.add_argument('--sender', action='store', help='alter the sender e.g.: --sender "Briefträger Willy <willy@example.com>"')
    mailgroup.add_argument('--footer', action='store', help='alter the footer (use quotes, and \\n for newlines)')

    aspsmsgroup.add_argument('--origin', action='store', help='alter the originator e.g.: \'Willy\' or \'+123456789\'')
    aspsmsgroup.add_argument('--flashing', action='store_true', default=False, help='send flashing sms')
    aspsmsgroup.add_argument('--maxchars', action='store', default=sample_settings['aspsms_maxchars'], type=int, help='split into several messages after N characters (default: %d)' %(sample_settings['aspsms_maxchars']))

    gsmsmsgroup.add_argument('--baud', action='store', default=115500, type=int, help='set the BAUD rate')

    twittergroup.add_argument('--mention', action='store', nargs='*', help='mention @user')

    args = parser.parse_args()

    functions[args.type](args)

if __name__ == '__main__':
    main()
