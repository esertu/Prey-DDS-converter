# Prey DDS converter v1.1 by esertu
# method originally devised by HeliosAI and not a russian spy on the XeNTaX forums
# now with system arguments and a GUI

print("Prey DDS converter v1.2")

import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import messagebox

##################

# establishing the basics of the GUI
root = Tk()
root.withdraw() #hidden by default
mainframe = ttk.Frame(root)

##################

# establishing variables
inputDir = StringVar()
inputDir.set("")
outputDir = StringVar()
outputDir.set("")
inputCopies = StringVar()
inputCopies.set("1")
applyToAll = BooleanVar() #this is for whether duplicate files are skipped or overwritten
applyToAll.set(True) #apply to all by default
proceedInput = StringVar() #this is for whether duplicate files are skipped or overwritten
convertState = StringVar()
convertState.set("")
infoTitle = StringVar()
infoText = StringVar()
infoTitle.set("")
infoText.set("")

outputFileNames = []
n = 0


#########

# function that asks for user input and then returns a sanitized version of that input (lowercase, with leading/ending square brackets removed)
def inputSan():
  origInput = input()
  retInput = origInput.lower().strip()
  if retInput.startswith("[") == True:
    retInput = retInput[1:]
  if retInput.endswith("]") == True:
    retInput = retInput[:-1]
  return(retInput)

# function that determines how to proceed when existing files are found - this is used three times so I've moved it up here to not clog up the script so much
def proceedCheck(fileName):
  print(f"Output file {fileName} already exists, please input how to proceed.")
  print("[s] - skip just this file")
  print("[sa] - skip all existing files (default)")
  print("[o] - overwrite just this file")
  print("[oa] - overwrite all existing files")
  proceedResult = inputSan()
  if proceedResult == "":
    proceedResult = "sa"
  elif proceedResult != "s" and proceedResult != "sa" and proceedResult != "o" and proceedResult != "oa":
    print("Input not recognized, defaulting to skipping all existing files.")
    proceedResult = "sa"
  return(proceedResult)

##################
# setting stuff up

exitConv = False
manual = False #this will determine whether the script asks the user a bunch of questions if there are no system arguments supplied
useGUI = True #this will determine whether or not the GUI is launched
arguments = {
  "input": False,
  "output": False,
  "overwrite": False,
  "copyall": False,
  "manual": False
} #dict collecting what arguments have been supplied

# parsing system arguments
if len(sys.argv) > 1:
  for argument in sys.argv[1:]:
    if argument.lower() == "skipconverting":
      proceedInput.set("s")
      print("*** Debug: skipping all conversions")
    elif argument.lower().find("-input=") != -1:
      inputDir.set(argument[argument.find("-input=")+len("-input="):].strip())
      arguments["input"] = True
      useGUI = False
    elif argument.lower().find("-output=") != -1:
      outputDir.set(argument[argument.find("-output=")+len("-output="):].strip())
      arguments["output"] = True
      useGUI = False
    elif argument.lower().find("-overwrite=") != -1:
      useGUI = False
      overwriteArg = argument[argument.find("-overwrite=")+len("-overwrite="):].lower().strip()
      if overwriteArg == "skipall" or overwriteArg == "overwriteall":
        arguments["overwrite"] = True
        if overwriteArg == "skipall":
          proceedInput.set("sa")
        elif overwriteArg == "overwriteall":
          proceedInput.set("oa")
      else:
        print(f"Argument \"{argument}\" not recognized, valid inputs for overwrite: skipAll, overwriteAll")
        exitConv = True
    elif argument.lower().find("-copyall=") != -1:
      useGUI = False
      inputCopiesArg = argument[argument.lower().find("-copyall=")+len("-copyall="):].lower().strip()
      if inputCopiesArg == "yes" or  inputCopiesArg == "no":
        arguments["copyall"] = True
        if inputCopiesArg == "yes":
          inputCopies.set("2") #yes copies
        elif inputCopiesArg == "no":
          inputCopies.set("1") #no copies
      else:
        print(f"Argument \"{argument}\" not recognized, valid inputs for copyAll: yes, no")
        exitConv = True
    elif argument.lower().find("-manual") != -1:
      useGUI = False
      manual = True

# exiting out if the above encountered an error
if exitConv == True:
  sys.exit()

if useGUI == False:
  
  # setting input directory - if there are no system arguments this loops until a valid input directory has been found or is set to be created
  inputDirset = False
  while inputDirset == False:
    if arguments["input"] == False:
      print("Please enter input directory below:")
      inputDir.set(input())
    if os.path.exists(inputDir.get()):
      inputDirset = True
    else:
      print(f"Directory {inputDir.get()} does not exist. Please try again with a different folder.")
      if arguments["input"] != False:
        sys.exit()

  # setting output directory - if there are no system arguments this loops until a valid input directory has been found or is set to be created
  outputDirset = False
  outputDirCreate = ""
  while outputDirset == False:
    if arguments["output"] == False or outputDirCreate != "":
      print("Please enter output directory below (not in Prey game folder):")
      outputDir.set(input())
    if os.path.exists(outputDir.get()):
      if outputDir.get() == inputDir.get():
        print(f"Error: input and output directories cannot match. Please specify different output directory.")
        if arguments["output"] != False or arguments["input"] != False:
          sys.exit()
      else:
        outputDirset = True
    else:
      print(f"Directory {outputDir.get()} does not exist. Do you want to proceed with the script, creating the folder in the process?")
      print(f"[Y]es - create new folder {outputDir.get()}")
      print(f"[N]o - specify different output directory")
      outputDirCreate = inputSan()
      if outputDirCreate == "y" or outputDirCreate == "n":
        if outputDirCreate == "y":
          outputDirset = True
      else:
        print("Error: input for output directory creation not recognized, please try again.")
        if arguments["output"] != False:
          sys.exit()

  # checking how to proceed with broken and non-broken files
  copyProceedSet = False
  while copyProceedSet == False:
    if arguments["copyall"] == False:
      print("Would you like to have all readable .dds files in one place after running this script, including the non-broken ones shipped with the game?")
      print("[1] - no, keep everything as it is.")
      print("[2] - yes, copy all non-broken .dds files to the output directory.")
      inputCopies.set(inputSan())
    if inputCopies.get() == "1" or inputCopies.get() == "2":
      copyProceedSet = True
    else:
      print("Error: input for copy procedure for non-broken files not recognized, please try again.")
      if arguments["copyall"] != False:
        sys.exit()

  print("---------------------------")


##################
# all set up! conversion starts now!

def fileConvert():
  print("---------------------------")
  scriptJustStarted = True
  HasDotAFiles = False
  currentNumber = 0
  highestNumber = 0
  currentNumberDotA = 0
  highestNumberDotA = 0
  skipConverting = False
  convertState.set("")
  convertedSomething = False
  infoTitle.set("")
  infoText.set("")
  
  #resetting the skip/overwrite duplicate file variables for every subsequent run
  applyToAll.set(True) #apply to all by default
  proceedInput.set("")

  # iterating through the given input directory
  for path, dirs, files in os.walk(inputDir.get()):
    for file in files:
    
      # checking what extension this file has starts here
      ext = os.path.splitext(file)[-1].lower()
        
      # checking if the extension of this file is a digit or is a digit plus the letter a
      # in both cases we then check if that digit is the highest digit-ed extension this file has
      # this is all in order to find the file with the highest digit/ digit plus the letter a, which is the largest mip level of the file (smaller mip levels get discarded)
      if ext[1:].isdigit() == True:
        currentNumber = int(ext[1:])
        if currentNumber > highestNumber:
          highestNumber = currentNumber
      elif ext[1:-1].isdigit() == True:
        currentNumberDotA = int(ext[1:-1])
        if currentNumberDotA > highestNumberDotA:
          highestNumberDotA = currentNumberDotA

      if ext[-1:] == "a":
        HasDotAFiles = True

      if ext == ".dds":
        if scriptJustStarted == True:
          # if the script just started then the first DDS file we hit is ie Psi_Hypo_ddna.dds, the first DDS file in the folder. This means we don't do anything just yet as we won't gather the necessary data until we hit the *second* DDS file in the folder.
          fileName = file
          scriptJustStarted = False
          thisPath = path
        else:
          # if this file has dotA files then we need to repeat the following twice with slightly tweaked parameters for the second round, which will be the round that converts the gloss file
          if highestNumberDotA != 0 and HasDotAFiles == True:
            repeat = 2
          else:
            repeat = 1

          n = 0
          while n < repeat:
        
            # if highestNumber is 0, then this dds has no extra files and can just be opened by any dds viewer without having to be edited first, so we skip/copy it
            if (highestNumber != 0 and inputCopies.get() == "1") or (inputCopies.get() == "2"):
              # we are now on the next DDS file in this folder, ie we have gone from Psi_Hypo_ddna.dds -> Psi_Hypo_ddna.dds.1 -> ... -> are now at Psi_Hypo_diff.dds
              # this means we've checked all the available files for the previous DDS file and figured out which one of them has the highest number
              # now we can copy and edit the revelant info into from the previous DDS file and its associated highest number file into a new file in the output directory
              
              # creating the output folder based on input folder architecture
              folderToCreate = thisPath.replace(inputDir.get(),"") # cutting away the path to the root input folder so that all that remains is ie "\GameSDK\GameData\Libs\UI\Textures\danielle_note_images"
              folderToCreate = outputDir.get() + folderToCreate # adding that to the output directory path
              # creating the resulting folder if it doesn't already exist
              if not os.path.isdir(folderToCreate):
                os.makedirs(folderToCreate)
              
              
              # reading and writing the DDS file/s:
              # skipping or copying nonbroken DDS files, skipping any succeessive conversion steps
              if highestNumber == 0 and inputCopies.get() == "2":
                outputFileFullPath = os.path.join(folderToCreate, fileName)
                inputDDSFileFullPath = os.path.join(thisPath, fileName)
                outputFileNames = [fileName]
                
                # checking if output file already exists, in which case check how to proceed
                if os.path.exists(outputFileFullPath):
                  if proceedInput.get() != "sa" and proceedInput.get() != "oa":
                    if useGUI == True:
                      alertWindow(fileName)
                    else:
                      proceedInput.set(proceedCheck(fileName))
                # if output file doesn't exist, or it exists but has been chosen to be overwritten, proceed with copying the file now
                if proceedInput.get() != "s" and proceedInput.get() != "sa":
                  print(f"Copying nonbroken DDS file {fileName}")
                  skipConverting = True
                  convertedSomething = True
                  with open(outputFileFullPath,'wb') as outputFileContent: 
                    with open(inputDDSFileFullPath,'rb') as inputDDSFileContent:
                      outputFileContent.write(inputDDSFileContent.read())
                else:
                  print(f"Skipping file {fileName}")
                  skipConverting = True
              
              # converting broken DDS files
              if skipConverting == False:
                # defining initial names: normal file names and gloss file names
                # output files
                glossName = os.path.splitext(fileName)[0]
                glossName = glossName[:-5] +  "_gloss.dds" # replacing the "_ddna" with "_gloss" (not sure if that's the actual terminology used in dev, might also be _spec or something similar)
                outputFileNames = [fileName,glossName]
                outputFileFullPath = os.path.join(folderToCreate, outputFileNames[n]) # entire path of the output file (file name: ie russian_body_ddna.dds / russian_body_ddna_gloss.dds)
                
                # input files
                inputglossName = fileName + ".a"
                inputFileNames = [fileName,inputglossName]
                inputDDSFileFullPath = os.path.join(thisPath, inputFileNames[n]) # entire path of the input DDS file (file name: ie russian_body_ddna.dds / russian_body_ddna.dds.a.dds)
                
                # highest number files
                highestNumberFileName = fileName + "." + str(highestNumber) # just the file name of the input highest number file, ie russian_body_ddna.dds.7
                highestNumberDotAName = fileName + "." + str(highestNumberDotA) + "a" # just the file name of the input highest number file, ie russian_body_ddna.dds.7a
                highestNumberFileNames = [highestNumberFileName,highestNumberDotAName]
                inputNumberFileFullPath = os.path.join(thisPath, highestNumberFileNames[n]) # entire path of the input DDS highest number file (file name: ie russian_body_ddna.dds.7 / ie russian_body_ddna.dds.7a)
                
                # checking if output file already exists, in which case check how to proceed
                if (os.path.exists(outputFileFullPath) and proceedInput.get() != "sa" and proceedInput.get() != "oa"):
                    if useGUI == True:
                      alertWindow(fileName)
                    else:
                      proceedInput.set(proceedCheck(fileName))
                # if output file doesn't exist, or it exists but has been chosen to be overwritten, proceed with converting the file now
                if (os.path.exists(outputFileFullPath) and proceedInput.get() != "s" and proceedInput.get() != "sa") or (os.path.exists(outputFileFullPath) == False):
                  print(f"Converting {outputFileNames[n]}")
                  convertedSomething = True
                  # opening/creating the output file
                  if os.path.exists(outputFileFullPath):
                    open(outputFileFullPath, "w")
                  else:
                    open(outputFileFullPath, "x")
                  
                  # reading the input files into the output file
                  with open(outputFileFullPath,'wb') as outputFileContent: 
                    # step one: grabbing the header from the .DDS file
                    with open(inputDDSFileFullPath,'rb') as inputDDSFileContent:
                      # total number of bytes we need to read is 148 in decimal, or 94 in hex
                      # however we need to write some additional missing bytes to the gloss files
                      if n == 0: # this file is a normal DDS file
                        outputFileContent.write(inputDDSFileContent.read(28)) # reading everything up to the b'\x0A' at offset 1C
                      else: # this file is a gloss file
                        outputFileContent.write(b'\x44\x44\x53\x20') # writing 44 44 53 20 to the start of the file because that's missing from the .a file header
                        outputFileContent.write(inputDDSFileContent.read(24)) # reading everything up to the b'\x0A' at offset 1C-4 (since we manually wrote the four bytes 44 44 53 20 at the start of the file)
                      outputFileContent.write(b'\x01') # writing b'\x01' instead of b'\x0A' there
                      inputDDSFileContent.seek(1,1) # skipping past the b'\x0A' in the original file
                      outputFileContent.write(inputDDSFileContent.read(119)) # reading the remaining 119 bytes
                    # step two: grabbing the info from the file with the highest number
                    with open(inputNumberFileFullPath,'rb') as inputNumberFileContent:
                      outputFileContent.write(inputNumberFileContent.read())
                else:
                  print(f"Skipping file {outputFileNames[n]}")
                  convertedSomething = True
          
            n = n + 1
            skipConverting = False

          # at the very end of all this we save the new file name, ie in this case it would be Psi_Hypo_diff.dds, and reset everything for this new DDS file
          fileName = file
          HasDotAFiles = False
          currentNumber = 0
          highestNumber = 0
          currentNumberDotA = 0
          highestNumberDotA = 0
          
          thisPath = path # saving the new path to be used at the very *end* of the operation since this script runs when it hits a .dds file, which means if we saved the path at the *start* it would put the first .dds file in a new folder into the old folder

  if convertedSomething == False: #if this is False, no correct files were found (set to True upon conversion or skip of file)
    if useGUI == True:
      infoTitleLabel.config(foreground="red")
      infoTextLabel.config(foreground="red")
      infoTitle.set("Error:")
      infoText.set("no convertable files were found!")
    print("Error: no convertable files were found!")
  else:
    if useGUI == True:
      infoTitleLabel.config(foreground="green")
      infoTitle.set("Done!")
  print("Done!")


##################

# GUI




# getting the input/output directory and checking if everything is okay with the input+output directories
def openDirs(state):
  dial = filedialog.askdirectory()
  if state == "input":
    inputDir.set(dial)
  elif state == "output":
    outputDir.set(dial)
    
  if outputDir.get() == inputDir.get():
    infoTitleLabel.config(foreground="red")
    infoTextLabel.config(foreground="red")
    infoTitle.set("Error:")
    infoText.set("input and output directories cannot match. \nPlease specify different output directory.")
  else:
    infoTitle.set("")
    infoText.set("")
  if infoTitle.get() == "":
    if outputDir.get() != "" and inputDir.get() != "":
      convertButton.state(['!disabled'])
  else:
      convertButton.state(['disabled'])

# setting up the application icon
# https://stackoverflow.com/questions/42474560/pyinstaller-single-exe-file-ico-image-in-title-of-tkinter-main-window
datafile = "superprofessionalicon_a8C_icon.ico"
if not hasattr(sys, "frozen"):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)

def resource_path(relative_path):    
  try:       
      base_path = sys._MEIPASS
  except Exception:
      base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

def guiRun():
  # setting up the window
  root.title("Prey .DDS converter")
  root.iconbitmap(default=resource_path(datafile))
  mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

  # new row
  rowN = 1
  ttk.Label(mainframe, text="input path:").grid(column=1, row=rowN, sticky=E)
  ttk.Label(mainframe, textvariable=inputDir, background="lightGrey", width=40).grid(column=2, row=rowN, sticky=(W, E))
  ttk.Button(mainframe, text="browse", command=lambda:openDirs("input")).grid(column=3, row=rowN, sticky=W)

  # new row
  rowN = 2
  ttk.Label(mainframe, text="output path:").grid(column=1, row=rowN, sticky=E)
  ttk.Label(mainframe, textvariable=outputDir, background="lightGrey", width=40).grid(column=2, row=rowN, sticky=(W, E))
  ttk.Button(mainframe, text="browse", command=lambda:openDirs("output")).grid(column=3, row=rowN, sticky=W)

  # new row
  rowN = 3
  ttk.Checkbutton(mainframe, text='Copy all found DDS files to output directory, including non-broken ones?',variable=inputCopies,onvalue="2", offvalue="1").grid(column=2, columnspan=2, row=rowN, sticky=E)

  # new row
  rowN = 4
  global convertButton
  convertButton = ttk.Button(mainframe, text="Convert", command=fileConvert, state='disabled')
  convertButton.grid(column=3, row=rowN, sticky=W)

  # these labels display "input/output folder match" and "no files found" errors and "done!" message
  global infoTitleLabel
  infoTitleLabel = ttk.Label(mainframe, textvariable=infoTitle, wraplength=300, foreground="red")
  infoTitleLabel.grid(column=1, row=rowN, sticky=NE)
  global infoTextLabel
  infoTextLabel = ttk.Label(mainframe, textvariable=infoText, wraplength=300, foreground="red")
  infoTextLabel.grid(column=2, row=rowN, sticky=NW)

  # open dialog asking whether to skip or overwrite if file with matching filename is found in output directory
  #  print("[s] - skip just this file")
  #  print("[sa] - skip all existing files (default)")
  #  print("[o] - overwrite just this file")
  #  print("[oa] - overwrite all existing files")
  global alertWindow
  def alertWindow(fileName):
    ttk.Entry(root)   # something to interact with
    dlg = Toplevel(root)
    dlg.iconbitmap(default=resource_path(datafile))
    
    dlgF = ttk.Frame(dlg)
    dlgF.grid(column=0, row=0, sticky=(N, W, E, S))
        
    def decisionF(decision):
      if decision == "overwrite":
        proceedInput.set("o")
      else:
        proceedInput.set("s")
      if applyToAll.get() == True:
        proceedInput.set(proceedInput.get() + "a")
        
      # destroy alert window
      dlg.grab_release()
      dlg.destroy()

    ttk.Label(dlgF, text=f"Output file \"{fileName}\" already exists, please input how to proceed.").grid(column=1, columnspan=2, row=1)
    ttk.Checkbutton(dlgF, text='Apply decision to all duplicate files',variable=applyToAll,onvalue=True, offvalue=False).grid(column=1, columnspan=2, row=2)
    ttk.Button(dlgF, text="Skip this file (default)", command=lambda:decisionF("skip")).grid(column=1, row=3)
    ttk.Button(dlgF, text="Overwrite this file", command=lambda:decisionF("overwrite")).grid(column=2, row=3)

    dlg.protocol("WM_DELETE_WINDOW", lambda:decisionF("skip")) # intercept close button
    dlg.transient(root)   # dialog window is related to main
    dlg.wait_visibility() # can't grab until window appears, so we wait
    dlg.grab_set()        # ensure all input goes to our window
    dlg.wait_window()     # block until window is destroyed


  for child in mainframe.winfo_children(): 
      child.grid_configure(padx=5, pady=5)

  root.bind("<Return>", fileConvert)
  root.deiconify()
  root.mainloop()





##################


if useGUI == False:
  fileConvert()
  print("Press enter to exit.")
  input()
else:
  guiRun()


##################



# original posts dumped below for easy reference:
#https://web.archive.org/web/20230818083651/https://forum.xentax.com/viewtopic.php?f=10&t=16241
#Ok what you need:
#Noesis (huge thanks here to MrAdults for supporting the normal map format of these properly, even Photoshop doesn't like them much)
#Hex Editor
#Intel .dds plugin for Photoshop (for the specgloss map thingies)
#This .zip with headers:
#BC4_Headers.zip
#1. Textures are made of these files:
#Image

#The .dds contains the header info and i think smallest mip level, 1-8 files are increasing mips of the texture. Just take the biggest one (with the highest number, in this case 8, it is the most HD version)

#2. Open the .dds and the .8 file in HxD. Switch to the .8 file and select everything with ctrl+a, then copy it with ctrl+c.

#3. Switch to the .dds file and select everyting starting at Offset 94 to the end:
#(94 is important, if you do it at for eg 95 your texture will be shifted sidewards and not match the UV)

#Then simply paste with ctrl+p and save with ctrl+s.

#4. Open texture in Noesis and convert to your format of choice.
#You can alternatively open these in Photoshop using the Intel plugins mentioned above. For that open your texture in HxD again and change this small part from whatever it is to 01 (thanks to chrrox for figuring this out):

#5. You may have noticed that _ddn (normal maps) usually don't just have the 1-X files but also files called like 6a,7a,8a. 1-8 belong to normal map, 1a-8a belong to the gloss map.
#You have to convert it seperately (as far as i know anyway). I don't know where the game gets this header from, it isn't the .a file. I figured it's BC4 textures however and added a .zip to this post that has headers for the dimensions i came across in the files. The gloss maps here share the dimensions the normal maps have (4k normal map = 4k gloss map). So if it is 4k, open BC4_4k_header.dds and the .8a file in HxD, copy everything from the .8a file again and paste it below the header (offset 80). Save it under a new name you will find easy.
#Noesis displays these as plain white, but Photoshop with the linked plugins loads them fine.

#6. I noticed that for some reasons the normal map channels seem to be switched (red should be green, green should be red). If you don't do that shading might look quite bad in whatever software you render in.

#7. You're finally done and can load them all on your model! Yey!


#https://web.archive.org/web/20230817173646/https://forum.xentax.com/viewtopic.php?t=16241&start=45
#Actually THERE IS .a file (at least in my case) for glossy maps! But! It's corrupted! So, if you can fix it, it will work just like the rest(i mean that you will be able to do the same thing as with that 1kb .dds files). This also will allow you to WORK WITH GLOSSY MAPS IN NEOSIS!

#Here is the way how to solve the problem:

#1. Open the .a file in Hex Editor

#2. Paste 44 44 53 20 before other stuff that must go after it

#3. Save it

#4. Work with it like with .dds file from the step 2 of the original post
