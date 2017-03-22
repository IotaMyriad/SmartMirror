#Use the following command to determine what to set device_index too: cat /proc/asound/cards

#sudo pip3 install SpeechRecognition
#sudo easy_install pyaudio

import _thread
import subprocess
import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone()

with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))

r.energy_threshold = 500

while True: 
    with sr.Microphone() as source:
        print("Say something!")
        try:
            audio = r.listen(source)
        except sr.WaitTimeoutError as we:
            print("Hitting time out")
            continue

        print ("Got it! Now to recognize it!")

	# recognize speech using Microsoft Bing Voice Recognition
    BING_KEY = "11a5b6e3266f434ca89758db27105b2c" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    try:
        print("Microsoft Bing Voice Recognition thinks you said: " + r.recognize_bing(audio, key=BING_KEY))
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    print()
