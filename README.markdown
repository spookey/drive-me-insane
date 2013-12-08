# drive-me-insane


alerting, messaging ~ python

use this software as a platform to enable messaging and alerting to your software or scripts

this code is python3

## configuration

to build yourself a configuration change the sample values in `util.py` and execute it afterwards:

    python util.py

you should have a __config.json__ afterwards.

## cli

this is a command line interface for your scripts

syntax: see `python cli.py -h`

Simple mail example:
	
	python cli.py mail mail@example.com 'This is a test-message' --subject 'Test'

### mail

this uses a __smtp__ connection to a server configured.

syntax: see contents of `sample.py`

### aspsms (planned)

this uses the **[http://aspsms.ch/](http://aspsms.ch/ "aspsms") webservice**.

syntax: see contents of `sample.py`

#### todo

* More Channels

    * irc
    * gsmsms

* Documentation

:smiley_cat: :smile_cat: :smiley_cat:
