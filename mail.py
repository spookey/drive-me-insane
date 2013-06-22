# -.- coding: utf-8 -.-

from itertools import chain
from email import charset
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from mimetypes import guess_type
from os.path import abspath, basename, expanduser
from ssl import SSLError
from smtplib import SMTP_SSL, SMTP, SMTPException
from util import logger, getconf

def make_header(to, sender, cc, subject=None):
    # prevent python to encode utf-8 text in base64. using quoted printables instead
    charset.add_charset('utf-8', charset.QP, charset.QP, 'utf-8')
    result = MIMEMultipart()
    # result.preamble = 'whatever'
    result.add_header('To', ', '.join(to))
    cc and result.add_header('CC', ', '.join(cc))
    result.add_header('From', sender)
    if not subject: subject = getconf('email_subject')
    if not subject: subject = '☃'
    subject = '[' + subject + '] ' + formatdate(localtime=True) if getconf('email_subject_date') else '[' + subject + ']'
    result.add_header('Subject', subject)
    result.add_header('Date', formatdate())
    result.add_header('X-Mailer', 'Postbote Willy')

    return result

def make_mime_text(messagetext):
    if getconf('email_footer'):
        messagetext = '\n'.join([messagetext, '_' * 48, getconf('email_footer'), ''])
    return MIMEText(messagetext, 'plain', 'UTF-8')

def make_mime_file(filename):
    def get_mime_type(filename):
        content_type, encoding = guess_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        return content_type.split('/', 1)

    filename = abspath(expanduser(filename))
    basefilename = basename(filename)

    result = MIMEBase(*get_mime_type(filename))
    result.set_payload(open(filename, 'rb').read())
    result.add_header('Content-Disposition', 'attachment', filename=basefilename)

    encode_base64(result)

    return result

def ext_log(command, text, warn=False):
    logresult = command
    line = '%s: status: %d ~ %s' %(text, logresult[0], logresult[-1].decode('utf-8'))
    if warn: logger.warn(line)
    else: logger.info(line)

def dialup():
    try:
        session = SMTP_SSL()
        ext_log(session.connect(getconf('smtp_server')), 'SSL connection')
    except (SMTPException, SSLError) as e:
        logger.error('SMTP SSL error: %s' %(e))

        try:
            session = SMTP()
            ext_log(session.connect(getconf('smtp_server'), 587), 'connection')
            session.ehlo()
            ext_log(session.starttls(), 'startTLS')
            session.ehlo()
        except SMTPException as e:
            logger.error('SMTP startTLS error: %s' %(e))

            try:
                session = SMTP()
                ext_log(session.connect(getconf('smtp_server')), 'plaintext connection', warn=True)
            except SMTPException as e:
                logger.error('SMTP error: %s' %(e))
                logger.error('connection failed')
                print('connection failed')
                exit(0)
            else:
                return session

        else:
            return session

    else:
        return session


def send_mail(to, messagetext, subject=None, **opt):

    cc = opt.get('cc', [])
    bcc = opt.get('bcc', [])
    files = opt.get('files', [])
    sender = opt.get('sender', getconf('email_sender'))

    recipients = list(chain(to, cc, bcc))

    logger.info('~' * 23)
    logger.info('sending new mail using %s:\n%d recipients ~ %d cc, %d bcc | %d files' %(sender, len(recipients), len(cc), len(bcc), len(files)))

    message = make_header(to, sender, cc, subject)
    message.attach(make_mime_text(messagetext))
    [message.attach(make_mime_file(f)) for f in files]

    session = dialup()

    try:
        ext_log(session.login(getconf('smtp_user'), getconf('smtp_password')), 'login')
        session.sendmail(sender, recipients, message.as_string().encode('utf-8'))
        logger.info('mail sent')

    except SMTPException as e:
        logger.error('SMTP Error: %s' %(e))
    finally:
        ext_log(session.quit(), 'quit')

    logger.info('end mail')

if __name__ == '__main__':
    pass
