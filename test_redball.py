# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "127.0.0.1"


# Global variable to store the AudioRecognition module instance
RedBallRecognition = None
redball = None
memory = None


class RedBallRecognitionModule(ALModule):
    """ A simple module able to recognise worlds

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        self.tts.say("Je lance le module de reconnaissance de balle")
        redball = ALProxy("ALRedBallDetection",NAO_IP,9559)
        

        # Subscribe to the Wordrecognised event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("redBallDetected",
            "RedBallRecognition",
            "onredballDetected")

    def onredballDetected(self, *_args):
        """ This will be called each time the ball is recognised.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("redBallDetected","RedBallRecognition")

        tts.say("Red ball detected")



        memory.subscribeToEvent("redBallDetected",
            "RedBallRecognition",
            "onredballDetected")

    def disconnect():
            redball = None
            tts = None

        



def main():
    """ Main entry point

    """
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





    # Warning: RedBallRecognition must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global RedBallRecognition
    RedBallRecognition = RedBallRecognitionModule("RedBallRecognition")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        RedBallRecognition.disconnect
        RedBallRecognition = None
        sys.exit(0)



if __name__ == "__main__":
    main()



