# -*- encoding: UTF-8 -*-
# Contient el module de suivi de balle

NAO_IP = "127.0.0.1"
NAO_PORT = 9559
memory = None

from naoqi import ALProxy
from naoqi import ALModule
import threading
import time
import math

# Permet de générer un thread s'occupant de gérer le suivi de balle et notamment de la perte de balle
class maThread(threading.Thread):
    def __init__(self, *args):
        """Initialisation de la thread, partie qui ne se joue qu'une seule fois."""
        threading.Thread.__init__(self)
        self.running = True
        self.lost = False
        self.countLost = 0
        global memory
        memory = ALProxy("ALMemory")
        self.motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
        self.postureProxy= ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
        self.redBallTracker = ALProxy("ALRedBallTracker", NAO_IP, NAO_PORT)


        

    def run(self):
        """Partie de programme qui se répète."""
        global memory
        self.postureProxy.applyPosture("Sit",0.5)
        self.motionProxy.setStiffnesses("Head", 1.0)
        self.redBallTracker.startTracker()
        while self.running == True:
            #print "Bam : "+str(self.lost)
            if self.lost == False:

                #data = memory.getData("redBallDetected",1)
                
                if self.redBallTracker.isNewData():
                    position = self.redBallTracker.getPosition()
                    self.lost = False
                    #print "Position : "
                    #print "   x = "+str(position[0])+" y = "+str(position[1])+" z = "+str(position[2])
                    self.countLost = 0
                else:
                    # S'il n'y a pas de nouvelles données, la balle est perdue de vu et on attends 10 itérations histoire d'être sur
                    self.countLost=self.countLost+1
                    #print "CountLost = "+str(self.countLost)
                    time.sleep(1.0)

                    if (self.countLost > 5):
                        print "Balle perdue"
                        self.lost = True
                        self.countLost = 0


            if self.lost == True:
            		# Dans le cas ou la balle est perdue de vue, on fait des mouvement de la tête pour la retrouver
                    #TODO : faire un mouvement de la tête et des bras cool
                    

                    self.motionProxy.setAngles("HeadYaw", 0, 0.3)
                    self.motionProxy.setAngles("HeadPitch", 0, 0.3)
                    time.sleep(1.0)



                    self.motionProxy.setAngles("HeadPitch",0.5, 0.3)
                    time.sleep(0.5)
                    self.motionProxy.setAngles("HeadYaw", 1, 0.5)
                    time.sleep(1.2)
                    if self.redBallTracker.isNewData():
                        self.lost = False
                    else:
                        self.motionProxy.setAngles("HeadYaw", -0.70, 0.5)
                        time.sleep(1.0)
                    
                        if self.redBallTracker.isNewData():
                            self.lost = False
                        else:

                            self.motionProxy.setAngles("HeadPitch",-0.5, 0.3)
                            time.sleep(0.5)
                            self.motionProxy.setAngles("HeadYaw", 0.70, 0.5)
                            time.sleep(1.0)

                            if self.redBallTracker.isNewData():
                                self.lost = False
                            else:
                                self.motionProxy.setAngles("HeadYaw", 0, 0.3)
                                self.motionProxy.post.setAngles("HeadPitch", 0, 0.3)
                                time.sleep(1.0)


    def stop(self):
        """Permet un arrêt propre de la thread."""
        
        print "Print BBB"
        self.redBallTracker.stopTracker()
        self.redBallTracker = None
        self.running = False
        


class RedBallRecognitionModule(ALModule):

    tts = None
    redBallTracker = None
    motionProxy = None
    postureProxy = None

    def __init__(self, name):
        ALModule.__init__(self, name)
        self.threadgestion = maThread()
        self.premierefois = True
        

    def disconnect(self, *_args):
        if self.threadgestion != None:
            if (self.threadgestion.running == True):
                print "AAA"
                self.threadgestion.stop()
                self.threadgestion.join(1) #1s de Timeout pour arrêter le thread
                self.threadgestion = None


    def connect(self, *_args):

        if self.premierefois == True:
            self.threadgestion.start()
            self.premierefois = False
        else:
            self.threadgestion = maThread()
            self.threadgestion.start()



    def grabTarget(self, *_args):


    	global memory
        memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
        self.postureProxy= ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
        self.redBallTracker = ALProxy("ALRedBallTracker", NAO_IP, NAO_PORT)


    	if self.threadgestion.lost == False:

            objectPos =  self.redBallTracker.getPosition()

            print "Position : "
            print "   x = "+str(objectPos[0])+" y = "+str(objectPos[0])+" z = "+str(objectPos[0])
            # # determine if the ball is withing reach so that it can be hit
            # if (objectPos[0] <= 0.2 and objectPos[1] >= -0.08 and objectPos[1] <= 0.08):
            #     # ball is in the middle
            #     print "ball is in the middle"

            # if (objectPos[0] <= 0.18 and objectPos[1] > 0.08):
            #     # ball is on the left
            #     print "ball is in the left"

            # if (objectPos[0] <= 0.18 and objectPos[1] < -0.08):
                # ball is on the right
            print "ball is in the right"
            jointSpeed = 0.2
            names = "Body"
            stiffness = 1.0
            self.motionProxy.stiffnessInterpolation(names, stiffness, 1.0)

            # Bow the head slightly
            self.motionProxy.setAngles("HeadPitch", 1.57/5, jointSpeed)

            # Initial rotation value of the hand for grabbing
            self.motionProxy.setAngles("RWristYaw", 0.5, jointSpeed)
            time.sleep(2.0)
             # Open the hand to grab the object
            self.motionProxy.setAngles("RHand", 0, jointSpeed)

             # Calculate the inverse kinematics for movement

            px = objectPos[0]   
            py = objectPos[1]   
            pz = objectPos[2]   


        
            
            if px == 0:
                theta1 = 0
            else:
                theta1 = math.atan(py/px)
            
            if pz == 0:
                theta2 = 0
            else:
                theta2 = math.atan((math.cos(theta1)*px +math.sin(theta1)*py)/pz)
            if(math.sin(theta1)*px-math.cos(theta1)*py ) == 0:
                theta3 = 0
            else:
                theta3 = math.atan((math.cos(theta1)*math.cos(theta2)*px+math.sin(theta1)*math.cos(theta2)*py - math.sin(theta2)*pz)/(math.sin(theta1)*px- math.cos(theta1)*py))
            if pow(math.cos(theta3),2)-pow(math.sin(theta3),2) == 0:
                theta4 = 0
            else:
                theta4 = 1/(pow(math.cos(theta3),2)-pow(math.sin(theta3),2))

   
            self.motionProxy.setAngles("RShoulderPitch", theta1, jointSpeed)
            self.motionProxy.setAngles("RShoulderRoll", theta2, jointSpeed)
            self.motionProxy.setAngles("RElbowYaw", theta3, jointSpeed)
            self.motionProxy.setAngles("RElbowRoll", theta4, jointSpeed)
            
            time.sleep(0.2)

            # Open the hand
            time.sleep(1)
            self.motionProxy.setAngles("RHand", 1, jointSpeed)
            self.tts.say("Je l'ai eu Youpi")
            
            # Get closer to grab the object (Adjust some of the inverse kinematics errors)

            # else:
            #     self.tts.say("La balle est hors d'atteinte")
            #     time.sleep(5.0)
            #     self.grabTarget(self)




