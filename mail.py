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
from ssl import SSLError, SSLContext, PROTOCOL_SSLv3
from smtplib import SMTP_SSL, SMTP, SMTPException
try:
    from util import logger, getconf
except ImportError:
    from .util import logger, getconf

def make_header(to, sender, cc, subject=None, subjecttag=None, subjectdate=None):
    # prevent python to encode utf-8 text in base64. using quoted printables instead
    charset.add_charset('utf-8', charset.QP, charset.QP, 'UTF-8')
    result = MIMEMultipart()
    # result.preamble = 'whatever'
    result.add_header('To', ', '.join(to))
    cc and result.add_header('CC', ', '.join(cc))
    result.add_header('From', sender)
    if not subject: subject = getconf('email_subject')
    if not subject: subject = '☃'
    subject = '[' + subjecttag + '] ' + subject if subjecttag else subject
    subject = subject + ' ' + formatdate(localtime=True) if subjectdate else subject
    result.add_header('Subject', subject)
    result.add_header('Date', formatdate())
    result.add_header('X-Mailer', 'Postbote Willy')

    return result

def make_mime_text(messagetext, footer=None):
    if footer:
        messagetext = '\n'.join([messagetext, '_' * 48, footer, ''])
    return MIMEText(messagetext, 'plain', 'UTF-8')

def make_mime_file(filename):
    def get_mime_type(filename):
        content_type, encoding = guess_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        return content_type.split('/', 1)

    filename = abspath(expanduser(filename))
    basefilename = basename(filename)

    with open(filename, 'rb') as f:
        result = MIMEBase(*get_mime_type(filename))
        result.set_payload(f.read())
        result.add_header('Content-Disposition', 'attachment', filename=basefilename)

        encode_base64(result)

        return result

def ext_log(command, text, warn=False):
    logresult = command
    line = '%s: status: %d ~ %s' %(text, logresult[0], logresult[-1].decode('UTF-8'))
    if warn: logger.warning(line)
    else: logger.info(line)

def dialup():
    context = SSLContext(PROTOCOL_SSLv3)
    def _ssl():
        sslsession = SMTP_SSL(context=context)
        ext_log(sslsession.connect(getconf('smtp_server'), getconf('smtp_port')), 'SSL connection')
        return sslsession
    def  _starttls():
        tlssession = SMTP()
        ext_log(tlssession.connect(getconf('smtp_server'), getconf('smtp_port')), 'startTLS connection')
        tlssession.ehlo()
        if tlssession.has_extn('STARTTLS'):
            ext_log(tlssession.starttls(context=context), 'startTLS')
            tlssession.ehlo()
            return tlssession
        else:
            logger.warning('plaintext connection')
            return tlssession

    try:
        if getconf('smtp_use_ssl'):
            session = _ssl()
        else:
            session = _starttls()

        ext_log(session.login(getconf('smtp_user'), getconf('smtp_password')), 'login')
        return session

    except (SMTPException, SSLError) as ex:
            logger.error('SMTP error: %s' %(ex))

def send_mail(to, messagetext, subject=None, **args):

    cc = args.get('cc', [])
    bcc = args.get('bcc', [])
    recipients = list(chain(to, cc, bcc))
    sender = args.get('sender', getconf('email_sender'))
    if not sender: sender = getconf('email_sender')
    footer = args.get('footer', getconf('email_footer'))
    if not footer: footer = getconf('email_footer')
    subjecttag = args.get('subjecttag', getconf('email_defaulttag'))
    subjectdate = args.get('subjectdate', getconf('email_subject_date'))
    files = args.get('files', [])

    logger.info('~' * 23)
    logger.info('sending new mail using %s:\n%d recipients ~ %d cc, %d bcc, %d files' %(sender, len(recipients), len(cc), len(bcc), len(files)))

    message = make_header(to, sender, cc, subject, subjecttag, subjectdate)
    message.attach(make_mime_text(messagetext, footer))
    [message.attach(make_mime_file(f)) for f in files]

    session = dialup()

    if session is not None:
        try:
            session.sendmail(sender, recipients, message.as_string().encode('UTF-8'))
        except SMTPException as ex:
            logger.error('smtp error: %s' %(ex))
            return ex
        else:
            logger.info('mail sent')
            return True
        finally:
            ext_log(session.quit(), 'quit')

    logger.info('end mail')
