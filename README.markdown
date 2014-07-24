# notify

mail and sms alert in python

use this software as a platform to enable messaging and alerting to your software or scripts

this code is python3

## configuration

to build yourself a configuration change the sample values in `util.py` and execute it afterwards:

    python3 util.py

you should have a __config.json__ afterwards.

twitter: 
generate an api key on [dev.twitter.com](https://dev.twitter.com "twitter dev") or ask me for mine.

enter the keys in `util.py` then run `python3 twitter.py` to generate oauth credentials.

## cli

this is a command line interface for your scripts

syntax: see `python cli.py -h`

Simple mail example:
	
	python3 cli.py mail mail@example.com 'This is a test message' --subject 'Test'

Mail to multiple recipients:

    python3 cli.py mail one@example.com two@example.com \
    'There is an attached file' \
    --cc three@example.com \
    --subject 'Test' \
    --sender 'Command Line <user@host.org>' \
    --files README.markdown

Simple aspsms example:

    python3 cli.py aspsms 0491234567890 'This is a test message' 

Simple twitter example:

    python3 cli.py twitter 'This is a test message' --mention user1 user2

### mail

this uses a __smtp__ connection to a server configured.

syntax: see contents of `sample.py`

### aspsms

this uses the [http://aspsms.ch/](http://aspsms.ch/ "aspsms") __webservice__.

requires [python-requests](http://python-requests.org/ "python-requests") module.

syntax: see contents of `sample.py`

### twitter

posts http messages to twitter using oauth.

requires [requests-oauthlib](https://requests-oauthlib.readthedocs.org/en/latest/ "python-requests-oauthlib") module.

syntax: see contents of `sample.py`

#### todo

* More Channels

    * irc
    * gsmsms

* Documentation

:smiley_cat: :smile_cat: :smiley_cat:
