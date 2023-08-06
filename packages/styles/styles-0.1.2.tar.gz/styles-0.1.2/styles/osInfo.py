"""
This Program is for getting os info and making commands,

if you make a terminal, you can use this for getting a ip
time, and other useful things, like this:   user@ip
"""
#imports:
import time, os
from styles import Style



#this will make a linux looking user line: <user>@<ip>
def simpleLinuxUser(user=str("")):
    """
    This this make a simple user and ip output,

    user:      the users name

    if "user" is left empty, this will use the windows logged in user
    otherwise "user" is what you gona see before ip: <user>@<ip>
    ip can't get changed, it will always what the pc have

    this also will give a <user> a bold font style,
    and <@ip> a cyan font style from styles.Style
    also ending on the same line, and with default color
    """
    if user == "":
        user = "Windows logged in User"
    
    print(Style.Colors["BOLD"] + user + Style.Colors["CYAN"] + "@ip:", Style.Colors["ENDC"] + " ", sep="", end="")


#this will make a linux looking user line: <user>@<ip>\n
def simpleLinuxUserNL(user=str(""), newLine=int(1)):
    """
    This is just like "simpleLinuxUser" but NL is for newLine

    user:     user name, or what user is logged in
    newLine:  How many times this will make a new line after user details

    this might give an error if you just do: simpleLinuxUserNL(5)
    you need to do: simpleLinuxUserNL(newLine=5)

    this will make a output looking like this:  <user>@<ip> :and end with
    newLineCommand * newLine number

    in this you can only change user and new line
    """
    if user == "":
        user = "Windows logged in User"
    
    nl = ""
    for x in range(newLine):
        nl = nl + "\n"

    print(Style.Colors["BOLD"] + user + Style.Colors["CYAN"] + "@ip:", Style.Colors["ENDC"] + " ", end=nl)