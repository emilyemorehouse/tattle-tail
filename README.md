TattleTail
==========
A Python script you can run while you're away to notify you if your dog barks.

Installation / Getting started
------------------------------
### Requirements
To run the program, you must have PortAudio installed. They have great documentation on this
process, check it out [here](http://portaudio.com/docs/v19-doxydocs/tutorial_start.html).

Next, install Python's requirements ([virtualenvwrapper](virtualenvwrapper.readthedocs.org) is
always recommended).

	$ pip install -r requirements.txt

You will need a [Firebase](firebase.google.com) account and a [OneSignal](onesignal.com) account if
you wish to track your sessions and receive push notifications (respectively). For more information
on setting these accounts up and retrieving your keys, check out the
[Firebase section](#setting-up-firebase) and [OneSignal section](#setting-up-onesignal).

Additionally, there is a [mobile app companion](emilyemorehouse/TattleTail.mobile) that registers
your device for push notifications, allows you to view session details, and analyzes your dog's
behavior.

### Configuration
There are a few configuations found in `config.py` that are integral, including:
* `AMBIENT_DB`: the ambient noise level in your home (more on this in the [calibration section](#calibrating-your-script))
* `ONESIGNAL_KEY`
* `ONESIGNAL_APP_ID`
* `FIREBASE_URL`

As well as some optional ones:
* `DEBUG`: this can be set to either `True` or `False`, it allows you to save data in Firebase to
either a production or development environment
* `PUSH_TIMER`: the minimum number of minutes between push notifications, used for throttling
* `DOGNAME`: your sweet pooch's name

### Running TattleTail
Once these things are set, you're ready to start tracking:

	$ python tattletail.py

Setting Up Firebase
-------------------
~COMING SOON~

Setting Up OneSignal
--------------------
~COMING SOON~

Calibrating Your Script
--------------------
~COMING SOON~
