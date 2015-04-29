# -*- encoding: UTF-8 -*-
import time
from main import *
RedBall = None

def StateManager(AudioRecognition):
	global RedBall
	MotReconnu = AudioRecognition.mot
	tts = AudioRecognition.tts
	Redball = None
	motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)

	if AudioRecognition.Redballactif == False:
		RedBall = RedBallRecognitionModule("RedBall")
		AudioRecognition.Redballactif = True



	if (MotReconnu == "Dis bonjour Naomie"):
		tts.say("Bonjour maître")
		print "Current State :"
		print AudioRecognition.cs

	if (MotReconnu == "Suis la balle"):
		if (AudioRecognition.cs == 0):
			tts.say("Je suis à vos ordre ")
			AudioRecognition.cs = 1
			RedBall.connect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 1):
			tts.say("Je suis déja la balle du regard abruti !")
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 2):
			tts.say("D'accord j'arrête d'essayer de l'attraper")
			AudioRecognition.cs = 1
			RedBall.disconnect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

	if (MotReconnu == "Attrape"):
		if ( AudioRecognition.cs == 1):
			tts.say("D'accord je vais essayer de l'attraper")
			AudioRecognition.cs = 2
			RedBall.grabTarget(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 2):
			tts.say("J'essaye déjà de l'attraper mongol")
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 0):
			tts.say("Fais moi d'abord suivre la balle")
			print "Current State :"
			print AudioRecognition.cs
			return


	if (MotReconnu == "On ne joue plus"):
			motionProxy.setStiffnesses("Body",0)
			tts.say("Ca marche")
			AudioRecognition.cs = 0
			RedBall.disconnect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return


	if AudioRecognition.cs == 0:
		RedBall.disconnect(RedBall)

	
	