# -*- encoding: UTF-8 -*-
# Generalites du robot
NAO_IP = "127.0.0.1"
NAO_PORT = 9559

# Global variable to store the memory module instance
memory = None

from StateManager import *
from naoqi import ALProxy
from naoqi import ALModule

class AudioRecognitionModule(ALModule):

    tts = None
    mot = "Rien"
    cs = 0
    asr = None


    def __init__(self, name, redball):
        ALModule.__init__(self, name, redball)
        self.tts = ALProxy("ALTextToSpeech")
        self.Redball = redball


    def disconnect(self, *_args):
        global asr
        global memory
        if (self.asr != None):
            self.asr.unsubscribe("ALSpeech")
            self.asr = None
            #memory.unregisterModuleReference("AudioRecognition")
            memory = None
            self.tts = None
            self.Redball = None

            # TODO : Stop the ASR engine properly

    def connect(self, *_args):
        if self.asr != None:
            self.disconnect(self)

        self.tts.setLanguage("English")
        self.tts.say("Hi everyone")
        self.tts.setLanguage("French")
     

        # Connecting to the Speech recognition module
        self.asr = ALProxy("ALSpeechRecognition",NAO_IP,NAO_PORT)
        # Set the language of recognition to French
        self.asr.setLanguage("French")
        # Enable to make a bip is played at the beginning of the recognition process, 
        # and another bip is played at the end of the process. 
        # self.asr.setAudioExpression(True)

        # The words that have to be recognised by the robot
        wordList=["On ne joue plus","Suis la balle","Attrape la balle","Dis bonjour Naomie"]
        # We update the vocabulary list
        # Warning : will crash if the ASR engine is still running
        #asr.setVocabulary(wordList,False)

        # Says the word that can be recognised
        #self.tts.say("Les actions pouvant etre reconnus sont") 
        #for index in range(0,len(wordList)):
        #    self.tts.say(wordList[index])

        # Subscribe to the Wordrecognised event
        self.asr.subscribe("ALSpeech")

        # Subscribe to the Wordrecognised event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("WordRecognized",
            "AudioRecognition",
            "onWordRecognised")


    def onWordRecognised(self, *_args):
        """ This will be called each time a word is recognised.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("WordRecognized","AudioRecognition")

        # We access to the word recognised in the memory
        word = memory.getData("WordRecognized")

        # Debug : Print the word recognised
        print("Mot :")
        print(word[0])
        print("Indice de confiance :")
        print(word[1])
        print


        # We acknoledge a word if the trust is high enough
        if (word[1] > 0.30):
            self.mot = word[0]
            #self.tts.say("Le mot reconnu est :"+self.mot)
            StateManager(self)
    

        # Subscribe again to the event
        memory.subscribeToEvent("WordRecognized",
            "AudioRecognition",
            "onWordRecognised")



