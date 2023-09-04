#Imports
from typing import ContextManager
import openai
import os

OPENAIAPI = "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"
openai.api_key = OPENAIAPI

import GPT as GPT
import warnings
warnings.filterwarnings('ignore')

from os import system
import time
import random
from tkinter import *
from tkinter import messagebox


#functions
def screenclear():
  try:
    system("clear")
  except:
    system('cls')

def numlist(list):
  optionslist = ""
  numup = ""
  for i in range(len(list)):
    optionslist += str(f"{i + 1}. {list[i].title()}\n")
    numup += str(i + 1) + "\\"
  return (f"({numup[:-1]})"), optionslist


def wait():
  time.sleep(random.randint(1, 3))

def initsave():
  try:
    f = open("savefile.txt", "x")
    return False
    
    f.close()
  except:
    
    if os.path.getsize('savefile.txt') == 0:
      print("File is empty!") 
      return False
    else:
      return True
  
##TKinter functions
def updateDisplay():
  global story
  t["state"] = NORMAL
  t.delete("1.0", "end")
  t.insert(END,str(story))
  t["state"] = DISABLED


def submit():
  global userInput
  submitInt.set(1)
  userInput = user_inputvar.get()
  user_inputvar.set("")
  submitInt.set(0)


def save():
  global story
  global prompt
  SaveBtn["state"] = DISABLED
  SaveBtn["text"] = "Saving..."
  
  f = open("savefile.txt", "w")
  f.write(f"You are an intelligent story telling computer. You will guide the user on an incredible story using their inputs based on the story prompt {prompt}. You will answer every input given by the user and sign off every message with 'What happens next?'. If for whatever reason you cannot fulfill a request (be it containing sensitive content, content that goes against OpenAI policy or for any other reason), you will not break the immersion but simply reply that this cannot be done (explaining how this goes outside the bounds of the fictional world). IF the user enters the phrase 'End Story' you will wrap the story up and finish off with the line 'To be continued' \n")
  f.write("Print out an introduction to the fictional world, and a first location that the player finds themselves in.\n")
  f.write(prompt)
  f.write("\n")
  f.write(str(story))
  f.close()
  s = messagebox.showinfo(title="Saved Game", message = "Game saved successfully!")
  SaveBtn["state"] = NORMAL
  SaveBtn["text"] = "Save"
  print("Saved \n",prompt,"\n",str(story))

  

def storyDone():
  screenclear()
  root.destroy()
  print("Thanks for playing! If you pressed SAVE you can find your story in the 'story.txt' file. You can load any story from where you left off by placing it in the 'story.txt file' otherwise clear it to start a new story")
  system.exit()



##Start tkinter
root = Tk()
root.title("AdventureGPT")
root.geometry("640x800")

screenTitle = StringVar()
screenTitle.set('AdventureGPT')
user_inputvar= StringVar()
submitInt = IntVar()
userInput = ""


l = Label(root, textvariable = screenTitle, font = "50")
t = Text(root, state = DISABLED, font = "15")
user_input = Entry(root, textvariable = user_inputvar, font="20")
SubmitBtn = Button(root, text = "Submit", bd = '5',command = submit)
SaveBtn = Button(root, text = "Save", state = DISABLED, bd = '5',command = save)
ExitBtn = Button(root, text = "Exit", bd = '5',command = storyDone)


l.pack()
t.pack()
user_input.pack()
SubmitBtn.pack()
SaveBtn.pack()
ExitBtn.pack()   

##

#Setup AI and Clear error messages
print("Loading AI...")
try:
  openai.checkconnection()
except:
  pass

wait()
print("Loading GUI..")
wait()
loadSave = initsave()
if loadSave == True:
  print("Savefile found! Loading...")
  
else:
  print("No savefile found. Creating new savefile...")

wait()
screenclear()
print("Ready!", end="\r")
time.sleep(1)
print("        ", end="\r")



##Setup User Story
prompt = ""
story = ""
if loadSave == False:
  setup = False
  choice = 0
  options = [
      "Cyberpunk Adventure", "Medieval Adventure", "Pirate Adventure",
      "Create Your Own"
  ]
  
  while setup == False:
    try:
      numups, optionlist = numlist(options)
      story += str(optionlist)
      story += str(f"{numups}: ")

      updateDisplay()
      root.update_idletasks()

      
      SubmitBtn.wait_variable(submitInt)
      choice = int(userInput) - 1
      
      story = ""
      updateDisplay()
      
      while choice > len(options):
        print("Please select an option", end="\r")
        time.sleep(1)
        print("                           ", end="\r")
        time.sleep(1)
        screenclear()
        wait()
  
        numups = numlist(options)
        choice = int(input(f"{numups}: ")) - 1
  
      setup = True
      screenclear()
  
    except:
      print("Please select an option", end="\r")
      time.sleep(1)
      print("                           ", end="\r")
      screenclear()
      wait()
    
    
    
  
  ##Story
  story = ""
  if options[choice] == "Create Your Own":
    prompt = input("Enter the theme for your world: ")
    
  else:
    prompt = options[choice]


    ## Starter Prompt
  messages = [ {"role": "system", "content": 
                f"You are an intelligent story telling computer. You will guide the user on an incredible story using their inputs based on the story prompt {prompt}. You will answer every input given by the user and sign off every message with 'What happens next?'. If for whatever reason you cannot fulfill a request (be it containing sensitive content, content that goes against OpenAI policy or for any other reason), you will not break the immersion but simply reply that this cannot be done (explaining how this goes outside the bounds of the fictional world). IF the user enters the phrase 'End Story' you will wrap the story up and finish off with the line 'To be continued'"} ]
  
  messages.append({"role": "system", "content": "Print out an introduction to the fictional world, and a first location that the player finds themselves in."},)
  ##


if loadSave == True:
  f = open("savefile.txt", "r")
  overall = f.readlines()
  prompt = overall[2]
  messages = "".join(overall[3:]) 
  story += str(messages)
  print(overall)
  messages = [{"role": "system", "content": (f"{str(overall)} Do not rerepeat any of the content above - simply build upon it.")}]

  
  updateDisplay()

screenTitle.set(prompt.title())

root.update_idletasks()


if loadSave == False:
  reply = GPT.askGPT(openai, messages)
  story += f"Adventure GPT: {reply} \n\n"
  
  print(f"AdventureGPT: {reply} \n")
  updateDisplay()

root.update_idletasks()

while True:
  SaveBtn["state"] = NORMAL
  SubmitBtn.wait_variable(submitInt)
  message = str(userInput).capitalize()
  #message = str(input("User: ")).capitalize()
  #userInput = ""
  story += f"User: {message} \n\n"
  updateDisplay()

  root.update_idletasks()
  
  if message:
    messages.append(
        {"role": "user", "content": message},
    )
    reply = GPT.askGPT(openai, messages)
  
    story += f"Adventure GPT: {reply} \n\n"

  
  print(f"AdventureGPT: {reply} \n")
  messages.append({"role": "assistant", "content": reply})

  updateDisplay()


  root.update_idletasks()








root.mainloop()
































# ##Main Conversation
# history = GPT.askGPT(g4f, (
#     "Use this prompt to generate the start of a story which will allow the user to finish it.",
#     str(startPrompt)), False)
# print(history, flush=True, end='\n')
# print("\n")



# def updatedisplay(new_text):
#     display_label.config(text=new_text)

# def update_display_periodically():
#     updatedisplay(history)
#     window.after(1000, update_display_periodically) 


# update_display_periodically()

# window.mainloop()






# while True:
#   message = input("User: ")
#   while True:
#     try:
#       response = str(GPT.askGPT(g4f, (str(history), str(message)), False))
#       print(response, flush=True, end="")
#       history += response
#       print("\n")
  
#     except:
#       response = str(GPT.askGPT(g4f, (str(history), str(message)), False))
#       print(response, flush=True, end="\n")
#       history += response
