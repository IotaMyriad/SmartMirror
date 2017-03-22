#Use the following command to determine what to set device_index too: cat /proc/asound/cards

#sudo pip3 install SpeechRecognition
#sudo easy_install pyaudio

import _thread
import subprocess
import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone()
#set threhold level
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))
# obtain audio from the microphone

r.energy_threshold = 500

def playSound():
    subprocess.call(["cvlc -A alsa,none --play-and-exit --alsa-audio-device default speech2.mp3"], shell=True)

while True: 
    with sr.Microphone() as source:
        #r.non_speaking_duration = 0.2
        #r.pause_threshold = 0.3
        print("Say something!")
        #try:
            #audio = r.listen(source, timeout=1, phrase_time_limit=2)
        audio = r.listen(source)
        #except sr.WaitTimeoutError as we:
            #print ("Nothing was said")
            #continue
        print ("Got it! Now to recognize it!")
        #_thread.start_new_thread(playSound, ())

	# recognize speech using Microsoft Bing Voice Recognition
    BING_KEY = "11a5b6e3266f434ca89758db27105b2c" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    try:
        print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

'''
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
'''
