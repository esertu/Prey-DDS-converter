# this is just a helper exe that runs the exe with or the exe without the command prompt

versionNumber = "1.3"

import subprocess
import os
import sys

# https://stackoverflow.com/questions/42474560/pyinstaller-single-exe-file-ico-image-in-title-of-tkinter-main-window
# https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
fileNameA = "PreyDDSConverter_gui_" + versionNumber + ".exe"
fileNameB = "PreyDDSConverter_cmd_" + versionNumber + ".exe"

# if this file is running as an exe, it's the compiled version and we want to look for the necessary files in Temp
if sys.argv[0].strip().endswith("exe") == True:
  if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    exePath = sys._MEIPASS
  else:
    exePath = os.path.dirname(sys.executable)
# otherwise, it's the non-compiled version and we want to look for the necessary files in this same folder
else:
  if getattr(sys, 'frozen', False):
    exePath = os.path.dirname(sys.executable)
  elif __file__:
    exePath = os.path.dirname(__file__)

finList = []
if len(sys.argv) == 1:
  fullPath = os.path.join(exePath, fileNameA)
  finList.append(fullPath)
else:
  fullPath = os.path.join(exePath, fileNameB)
  finList.append(fullPath)
  for arg in sys.argv[1:]:
    finList.append(arg)

subprocess.run(finList)
