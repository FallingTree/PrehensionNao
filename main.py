# -*- encoding: UTF-8 -*-
import sys
import time
from AudioRecognitionModule import *
from TactileHeadModule import *
from redball import *


from naoqi import ALBroker
from optparse import OptionParser

# Generalites du robot
NAO_IP = "127.0.0.1"
NAO_PORT = 9559

# Global variable to store the AudioRecognition module instance
AudioRecognition = None
TactileHead = None


def main():
    """ Main entry point

    """
    global AudioRecognition
    global RedBall


    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port



    # Create proxy to ALTextToSpeech for later use
    # tts = ALProxy("ALTextToSpeech")

    # Warning: AudioRecognition must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    
    
    AudioRecognition = AudioRecognitionModule("AudioRecognition")
    AudioRecognition.connect(AudioRecognition)
    TactileHead = TactileHeadModule("TactileHead",AudioRecognition)


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        AudioRecognition.disconnect(AudioRecognition)
        AudioRecognition = None
        sys.exit(0)



if __name__ == "__main__":
    main()