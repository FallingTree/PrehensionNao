# -*- encoding: UTF-8 -*-

import time

from naoqi import ALProxy
from naoqi import ALProxy
from naoqi import ALModule

# Global variable to store the memory instance
memory = None

class TactileHeadModule(ALModule):
    AudioModule = None
    def __init__(self, name, audiomodule):
        ALModule.__init__(self, name)
        
        self.AudioModule = audiomodule

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("MiddleTactilTouched",
            "ReactToTouch",
            "onTouched")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("MiddleTactilTouched",
            "ReactToTouch")
        self.tts.say("D'accord, on arrête de jouer")
        self.AudioModule.cs = 0

        # Subscribe again to the event
        memory.subscribeToEvent("MiddleTactilTouched",
            "ReactToTouch",
            "onTouched")

