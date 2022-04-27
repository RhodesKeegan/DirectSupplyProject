import pyttsx3 as tts

# pip install pyttsx3 --- command to install the library

output = "You should check the connection between the temperature sensor and the PCB. " \
         "If that is fine, then measure the resistance of the sensor."

engine = tts.init()

# print(engine.getProperty('rate'))                    # prints out voice rate
engine.setProperty('rate', 170)                        # decreasing the voice rate from 200 (default) to 170

voices = engine.getProperty('voices')
# engine.setProperty(h'voice', voices[1].id)           # change voice from male (0) to female (1)

engine.say(output)                                     # pass in desired string and convert it into speech
engine.runAndWait()
engine.stop()


