import os
import eel

# from backend.commands import playAssistantSound
from backend.commands import *
from backend.commands import main
eel.init("D:/Ad_Voice_assistant/frontend")

# playAssistantSound()

os.system('start msedge.exe --app="http://localhost:8000/index.html"')

eel.start('frontend/index.html', mode = None, host='localhost', block=True)

start_assistant()



