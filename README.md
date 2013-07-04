# drive-me-insane


alerting, messaging ~ python

use this software as a platform to enable messaging and alerting to your software or scripts

not all libraries are python3 compatible, will fallback to 2.7 when necessary

## configuration

to build yourself a configuration change the sample values in `util.py` and execute it afterwards:

    /usr/bin/python util.py

you should have a `config.json` afterwards.

## cli

this is a command line interface for your scripts

syntax: see `python cli.py -h`

### mail

this uses a `smtp` connection to a server configured.

syntax: see contents of `sample.py`

### aspsms

this uses the [http://aspsms.ch/](http://aspsms.ch/ "aspsms") `soap` webservice.

this depends on `pysimplesoap`, install via:

    pip install --upgrade pysimplesoap

#### todo

* More Channels

* Documentation

:smiley_cat: :smile_cat: :smiley_cat:
