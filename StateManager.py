# -*- encoding: UTF-8 -*-
import time
from main import *

def StateManager(AudioRecognition):
	MotReconnu = AudioRecognition.mot
	tts = AudioRecognition.tts
	Redball = Audiorecognition.Redball

	if (MotReconnu == "Dis bonjour Naomie"):
		tts.say("Bonjour maître")
		print "Current State :"
		print AudioRecognition.cs

	if (MotReconnu == "Suis la balle"):
		if (AudioRecognition.cs == 0):
			tts.say("Je suis à vos ordre maître absolu")
			AudioRecognition.cs = 1
			RedBall.connect()
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
			RedBall.disconnect()
			print "Current State :"
			print AudioRecognition.cs
			return

	if (MotReconnu == "Attrape la balle"):
		if ( AudioRecognition.cs == 1):
			tts.say("D'accord je vais essayer de l'attraper")
			AudioRecognition.cs = 2
			RedBall.grabTarget()
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 2):
			tts.say("J'essaye déjà de l'attraper mongol")
			print "Current State :"
			print AudioRecognition.cs
			return

		if (AudioRecognition.cs == 0):
			tts.say("D'accord je vais essayer de l'attraper")
			AudioRecognition.cs = 2
			RedBall.grabTarget()
			print "Current State :"
			print AudioRecognition.cs
			return


	if (MotReconnu == "On ne joue plus"):
			tts.say("Ca marche mon pote")
			AudioRecognition.cs = 0
			RedBall.disconnect(RedBall)
			print "Current State :"
			print AudioRecognition.cs
			return

	
	