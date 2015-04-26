# -*- encoding: UTF-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "127.0.0.1"


# Global variable to store the AudioRecognition module instance
RedBallRecognition = None
NAO_IP = "127.0.0.1"
NAO_PORT = 9559
memory = None


class RedBallRecognitionModule(ALModule):

    tts = None
    redBallTracker = None
    motionProxy = None
    postureProxy = None
    lost = None
    actif = None
    countLost = 0


    def __init__(self, name):
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")
        self.lost = False
        self.actif = False

    def disconnect(self, *_args):
        if (self.redBallTracker != None):
            self.redBallTracker.stopTracker()
            print "Tracker Stopped"
            self.motionProxy.setStiffnesses("Head", 0.0)
            self.motion = None
            self.redBallTracker = None
            self.tts = None
            self.countLost = 0


    def connect(self, *_args):
        if (self.redBallTracker != None):
            self.disconnect()
        self.motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
        self.postureProxy= ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
        self.redBallTracker = ALProxy("ALRedBallTracker", NAO_IP, NAO_PORT)

        self.postureProxy.applyPosture("Sit",0.5)
        self.motionProxy.setStiffnesses("Head", 1.0)
        self.redBallTracker.startTracker()
        self.actif = True

        #TODO : Faire un trhread pour la gestion

        global memory
        memory = ALProxy("ALMemory")

    def gestion(self,*_args):
        global memory
        if (self.actif == True):
            if (self.lost == True):

                    #TODO : faire un mouvement de la teête et des bars cool
                    self.motionProxy.setAngles("HeadYaw", 0, 0.3)
                    self.motionProxy.setAngles("HeadPitch", 0, 0.3)
                    time.sleep(1.0)


                    self.motionProxy.setAngles("HeadPitch",0.5, 0.3)
                    time.sleep(0.5)
                    self.motionProxy.setAngles("HeadYaw", 1, 0.5)
                    time.sleep(1.2)
                    ide = self.motionProxy.post.setAngles("HeadYaw", -1, 0.5)
                    self.motionProxy.wait(ide, 10)
                    

                    self.motionProxy.setAngles("HeadPitch",-0.5, 0.3)
                    time.sleep(0.5)
                    ide = self.motionProxy.post.setAngles("HeadYaw", 1, 0.5)
                    self.motionProxy.wait(ide, 10)

                    self.motionProxy.setAngles("HeadYaw", 0, 0.3)
                    ide = self.motionProxy.post.setAngles("HeadPitch", 0, 0.3)
                    self.motionProxy.wait(ide, 10)


            else:

                data = memory.getData("redBallDetected",1)

                if self.redBallTracker.isNewData():
                    position = self.redBallTracker.getPosition()
                    self.lost = False
                    print "Position : "
                    print "   x = "+str(position[0])+" y = "+str(position[1])+" z = "+str(position[2])
                else:
                    self.countLost = self.countLost+1
                    print "CountLost = "+str(self.countLost)

                    if (self.countLost > 10):
                        print "Balle perdue"
                        self.lost = True
                        self.countLost = 0







                
        



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
    RedBallRecognition.connect()


    try:
        while True:
            time.sleep(1)
            RedBallRecognition.post.gestion()
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        RedBallRecognition.disconnect()
        RedBallRecognition = None
        sys.exit(0)



if __name__ == "__main__":
    main()



