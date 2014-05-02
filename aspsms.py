# -.- coding: utf-8 -.-

from requests import post as rpost
from textwrap import wrap
try:
    from util import logger, getconf
except ImportError:
    from .util import logger, getconf

xml_base = '''<?xml version="1.0"?>
<aspsms>
    <Userkey>{userkey}</Userkey>
    <Password>{password}</Password>
    <Originator>{originator}</Originator>
    <Recipient>
        <PhoneNumber>{to}</PhoneNumber>
    </Recipient>
    <MessageData>{text}</MessageData>
    <FlashingSMS>{flashing}</FlashingSMS>
    <Action>SendTextSMS</Action>
</aspsms>'''

def make_xml(to, originator, text, flashing):
    flashing = str(flashing).lower()
    return xml_base.format(
        userkey=getconf('aspsms_userkey'),
        password=getconf('aspsms_password'),
        originator=originator,
        to=to,
        text=text,
        flashing=flashing
        )

def post_xml(xmlpayload):
    headers = {'content-type': 'application/xml'}
    response = rpost(getconf('aspsms_gateway'), headers=headers, data=xmlpayload)
    return response.text

def response_xml(xml):
    xml = [outer.split('</') for outer in [inner.split('>') for inner in xml.split('\n') if 'aspsms' in inner][-1] if '</' in outer]
    result = dict()
    for val, key in xml:
        if val:
            result[key] = val
            logger.info('aspsms %s: %s' %(key, val))
    return result

def send_aspsms(to, messagetext, **args):

    originator = args.get('originator', getconf('aspsms_originator'))
    if not originator: originator = getconf('aspsms_originator')
    flashing = args.get('flashing', getconf('aspsms_flashing'))
    maxchars = args.get('maxchars', getconf('aspsms_maxchars'))

    logger.info('~' * 23)
    logger.info('sending new aspsms using %s:\n%d recipients ~ flashing: %s' %(originator, len(to), flashing))

    message = wrap(messagetext, maxchars)

    try:
        for recipient in to:
            for text in message:
                payload = make_xml(recipient, originator, text, flashing)
                response = response_xml(post_xml(payload))
                if not response['ErrorCode'] == '1':
                    raise Exception('aspsms error: %s' %(response['ErrorDescription']))
    except Exception as ex:
        logger.error('error: %s' %(ex))
        return ex
    else:
        logger.info('aspsms sent')
        return True

    logger.info('end aspsms')
