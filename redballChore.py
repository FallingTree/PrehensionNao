import time
import math
import motion

class RedBallRecognitionModule(ALModule):
    trackerProxy = None
    motionProxy =  None
    postureProxy =  None
    lost = True
    track = False
    threadTime = 0.2
    countLost = 0
    targetName = None
    hitBall = False
    prevXPos = 0.0                   # previous ball's position in the x axis
    prevYPos = 0.0 
    def __init__(self):
        self.trackerProxy = None
        self.motionProxy =  ALProxy("ALMotion")
        self.postureProxy =  ALProxy("ALRobotPosture")
        self.lost = True
        self.track = False
        self.threadTime = 0.2
        self.countLost = 0
        self.targetName = None
        self.hitBall = False
        self.prevXPos = 0.0                   # previous ball's position in the x axis
        self.prevYPos = 0.0                  # previous ball's position in the y axis


    def onLoad(self):
        self.bIsRunning = False
        self.timer = None

    def onUnload(self):
        if not self.timer:
            return

        self.timer.cancel()
        self.timer = None

        if self.trackerProxy:
            if self.trackerProxy.isActive():
                self.trackerProxy.stopTracker()

    def onStart(self):

        self.trackerProxy = ALProxy("ALRedBallTracker")
        if self.trackerProxy != None:
            if(not self.trackerProxy.isActive()):
                self.trackerProxy.startTracker()
                self.timer = threading.Timer(self.threadTime, self.getTargetInformation)
                self.timer.start()


    def onInput_onStop(self):
        if self.timer:
            self.onUnload()
            self.onStopped()

    def getTargetInformation(self):
        targetName = self.getParameter("Target choice")

        # Restart tracker with the new target if changed
        if self.targetName != targetName:
            self.onUnload()
            self.onInput_onStart()

        elif self.trackerProxy:
            if self.trackerProxy.isNewData():
                self.countLost = 0
                if not self.track:
                    self.track = True
                    self.lost = False
                    self.foundTarget()
                self.trackerProxy.getPosition()
                self.log(self.trackerProxy.getPosition())
                self.log(self.trackerProxy.getPosition()[0])
                #~ if (self.trackerProxy.getPosition()[0] < 0.2):
                    ##~ self.onUseBottomCamera()
                    #~ self.useTop()
                #~ else:
                    #~ self.useBottom()
                ALMemory.insertData("/RobotsLAB/ballInView", True)
                # determine if the ball is withing reach so that it can be hit
                if (self.trackerProxy.getPosition()[0] <= 0.2 and self.trackerProxy.getPosition()[1] >= -0.08 and self.trackerProxy.getPosition()[1] <= 0.08):
                    self.hitCenterBall()                             # ball is in the middle
                if (self.trackerProxy.getPosition()[0] <= 0.18 and self.trackerProxy.getPosition()[1] > 0.08):
                    self.hitLeftBall()                                 # ball is on the left
                if (self.trackerProxy.getPosition()[0] <= 0.18 and self.trackerProxy.getPosition()[1] < -0.08):
                    self.hitRightBall()                                 # ball is on the right    
                self.prevXPos = self.trackerProxy.getPosition()[0]    
                #self.prevYPos = self.
                self.log(self.trackerProxy.getPosition())
                self.log(self.trackerProxy.getPosition()[0])
                ALMemory.insertData("/RobotsLAB/ballPos", self.trackerProxy.getPosition())
                #self.grabTarget(self.trackerProxy.getPosition())
            else:
                self.log("lost?")
                ALMemory.insertData("/RobotsLAB/ballInView", False)
                self.countLost = self.countLost + 1
                if self.countLost*self.threadTime > self.getParameter("Time before lost (s)"):
                    if not self.lost:
                        self.lost = True
                        self.track = False
                        self.isLost()

        self.timer = threading.Timer(self.threadTime, self.getTargetInformation)
        self.timer.start()
        timer.sleep(1)

    def onUseTopCamera(self):
        self.cameraModule.setParam( self.kCameraSelectID, 0 )
        
    def onUseBottomCamera(self):
        self.cameraModule.setParam( self.kCameraSelectID, 1 )
    
    def grabTarget(self, targetPosition):                     # move arms to objects position
        motionProxy = ALProxy("ALMotion")
        #jointSpeed = targetPosition
        #objectPos =  ALMemory.getData("/RobotsLAB/objectPos")        
        jointSpeed = 0.2
        #names = "Body"
        #stiffness = 1.0
        #motionProxy.stiffnessInterpolation(names, stiffness, 1.0)
        # Bow the head slightly
        #motionProxy.setAngles("HeadPitch", 1.57/5, jointSpeed)
        # Initial rotation value of the hand for grabbing
        motionProxy.setAngles("LWristYaw", -0.5, jointSpeed)
        motionProxy.setAngles("RWristYaw", 0.5, jointSpeed)
         # Open the hand to grab the object
       # motionProxy.setAngles("RHand", 0, jointSpeed)
        
        # Point of movement until the arm comes down
        #point = [[1,-1,0.3], [1,-0.5,0.3], [1,0.01,0.3], [1,0.5,0.3], [1,0.7,0.3]]
        
         # Calculate the inverse kinematics for movement
        #for i in range(0,5):
        px = targetPosition[0]   #point[i][0]
        py = targetPosition[1]   #point[i][1]
        pz = targetPosition[2]   #point[i][2]
    
        self.log(px)
        self.log(py) 
        self.log(pz)
        
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
        
        self.log( theta1)
        self.log(theta2)
        self.log(theta3)
        self.log(theta4)
        
        motionProxy.setAngles("RShoulderPitch", theta1, jointSpeed)
        motionProxy.setAngles("RShoulderRoll", theta2, jointSpeed)
        motionProxy.setAngles("RElbowYaw", theta3, jointSpeed)
        motionProxy.setAngles("RElbowRoll", theta4, jointSpeed)
        
        time.sleep(0.2)
        #forloopend
        # Open the hand
        #time.sleep(1)
        #motionProxy.setAngles("RHand", 1, jointSpeed)
        
         # Get closer to grab the object (Adjust some of the inverse kinematics errors)