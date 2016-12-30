import analyse
import datetime
import helpers
import numpy
import pyaudio
import signal
import sys
from multiprocessing import Process
from config import DefaultConfig


# Hacky way to set Firebase endpoints for dev vs production
sessions_endpoint = 'sessions'
barks_endpoint = 'barks'
if DefaultConfig.DEBUG:
    print('DEBUG mode enabled')
    sessions_endpoint += '-dev'
    barks_endpoint += '-dev'
sessions_endpoint += '/'
barks_endpoint += '/'


def main():
    # Override the 'CTRL+C' handler in order to send end the session when the script is ended.
    # Store the original SIGINT handler

    original_sigint = signal.getsignal(signal.SIGINT)

    def end_session(*args):
        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                # Restore the original signal handler as otherwise evil things will happen
                # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
                signal.signal(signal.SIGINT, original_sigint)

                # Log session end and send push
                helpers.logEvent(sessions_endpoint + session['name'], {'session_ended': datetime.datetime.now().isoformat()}, id=True)
                helpers.sendPush('Session ended!')
                print('Session ended!')
                sys.exit(1)

        except KeyboardInterrupt:
            # Restore the original signal handler as otherwise evil things will happen
            # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
            signal.signal(signal.SIGINT, original_sigint)

            # Log session end and send push
            helpers.logEvent(sessions_endpoint + session['name'], {'session_ended': datetime.datetime.now().isoformat()}, id=True)
            helpers.sendPush('Session ended!')
            print('Session ended!')
            sys.exit(1)

    # Restore the exit gracefully handler here
    signal.signal(signal.SIGINT, end_session)

    # Set up our PyAudio handler
    p = pyaudio.PyAudio()

    # Set up variables used by PyAudio
    chunk = 1024
    sample_rate = int(p.get_device_info_by_index(0)['defaultSampleRate'])
    num_channels = p.get_device_info_by_index(0)['maxInputChannels']
    audio_format = pyaudio.paInt16

    # Set up our variables (these will be moved to config)
    ambient_db =  DefaultConfig.AMBIENT_DB                          # the ambience noise level in db
    min_push_limit = DefaultConfig.PUSH_TIMER                           # number of minutes between e-mails
    last_sent_time = None

    # Log session start and send push
    session = helpers.logEvent(sessions_endpoint, {'session_started': datetime.datetime.now().isoformat()})
    helpers.sendPush('Session started!')
    print('Session started!')

    # Open input stream
    stream = p.open(
        format=audio_format,
        channels=num_channels,
        rate=sample_rate,
        input=True)

    # Loop infinitely to process the data stream
    while True:
        raw_sample = stream.read(chunk, exception_on_overflow = False)      # Grab a raw chunk of data
        sample = numpy.fromstring(raw_sample, dtype = numpy.int16)          # Convert raw data to NumPy array
        loudness = analyse.loudness(sample)
        print loudness                              # Determine loudness of the data

        # If the loudness is greater than our ambient level, log the sound and send a notification
        if loudness > ambient_db:
            current_time = datetime.datetime.now()                          # Time at which the sound was detected

            # Log the noise whether we send a push or not
            p = Process(target=helpers.logEvent, args=(barks_endpoint, {'loudness': loudness, 'date': datetime.datetime.now().isoformat(), 'session_id': session['name']},))
            p.start()

            # Check to see when the last push was sent
            if(last_sent_time != None):
                time_delta = current_time - last_sent_time
            else:
                time_delta = datetime.timedelta(minutes=min_push_limit + 1)

            # Only send a push to the user if one hasn't been sent recently
            if (time_delta > datetime.timedelta(minutes=min_push_limit)):
                print("Loudness detected, sending push", str(current_time), loudness)

                # Update last sent time
                last_sent_time = current_time

                # sending the push is in a process so that it won't...cause things to crash
                p = Process(target=helpers.sendPush, args=(DefaultConfig.DOGNAME + " barked!",))
                p.start()
            else:
                print("Loudness detected, push already sent", str(current_time), loudness)


if __name__ == '__main__':
    main()
