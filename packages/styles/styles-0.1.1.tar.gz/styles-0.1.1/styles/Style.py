#imports:
import time



#extras:
#this part is googled becuse colors is complicated
Colors = {
    "HEADER": '\033[95m',
    "BLUE": '\033[94m',
    "CYAN": '\033[96m',
    "GREEN": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[96m'
}



#defs:
#this is a spinning loadingbar
def loadingbar_spinning(sleep=float(0.1), times=int(3), text=str("Loading: ")):
    """
    This is a loadingbar animation of a spinnign wheel

    sleep:  time delay before next character is printed
    times:  how many times the circle should spin around
    text:   set the text before loading

    ends with two new lines, and the default color
    """

    print(Colors["BOLD"] + text + " ", sep="", end="", flush=True)
    for x in range(times):
        for x in r"-\|/-\|/":
            print("\b", Colors["FAIL"] + x, sep="", end="", flush=True)
            time.sleep(sleep)
    
    print("\b|", Colors["ENDC"] + "\n\n")


#this is a loadingbar line
def loadingbar_line(sleep=float(0.1), times=int(51), text=str("Loading: ")):
    """
    This is a animation of a loadingbar line: ############

    sleep:  time delay before next character is printed
    times:  how many times to print "#"
    text:   set the text before loading

    ends with two new lines, and the default color
    """

    print(Colors["BOLD"] + text + " ", sep="", end="", flush=True)
    for x in range(times):
        print(Colors["FAIL"] + "#", sep="", end="", flush=True)
        time.sleep(sleep)
    
    print(Colors["ENDC"] + "\n\n")


#this is a other loadingbar line
def loadLineDL(sleep=float(0.1), text=str("Loading:")):
    """
    This loadingbar will look something like this:
    Loading: [#####     ] 50%

    this one will only count: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100

    sleep:  time delay before next character is printed
    text:   set the text before loading, by default it has not space

    this time you can not change amount of characters to print
    it will always print "##" 10 times: ####################

    ends with two new lines, and the default color

    the name DL is for Download Line
    """

    t = ""
    space = "                    "
    for x in range(10):
        procent = x * 10
        t = t + "##"
        space = (space + "\b\b")
        line = (t + space)

        print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + f"{procent}%", end="\r")
        time.sleep(sleep)
    
    #at the end print the hole line
    print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + "100%\n\n")


#this is a loadingbar line with download style, but this one can count 1 and 10
def loadLineDSE(sleep=float(0.1), text=str("Loading:")):
    """
    This is almost like styles.loadingLineDL but this one can count with 1
    
    sleep:  time delay before next character is printed
    text:   text before loading, default look: Loading: [######    ] 60%

    this loadingbar will load from 1 - 100%, it will have [#####   ]
    and a text displaying what "text" is set to

    this function will exit with two new lines

    "DSE" is for "Download Style Enter", dont really know what E is for yet
    """

    #extras:
    t = ""
    space = "                   "
    procent = 1
    prev = 0

    #loadingbar loop
    for x in range(100):
        #setting everything
        procent = x

        #this is set only when to aply more "###" to loadingbar line
        if prev == 0:
            prev = x
        elif (x - prev) == 5:
            t = t + "#"
            space = (space + "\b")
            
            prev = x

        line = (t + space)

        #printing the line and waiting for "sleep" amount of seconds
        print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + f"{procent}%", end="\r")
        time.sleep(sleep)
    
    #end
    print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + "100%\n\n")


#this is a loadingbar line with download style, but this one can count 1 and 10, and it uses "-"
def loadLineDSEL(sleep=float(0.1), text=str("Loading:")):
    """
    This is almost like styles.loadLineDSE but this one uses "-" and not "#"
    
    sleep:  time delay before next character is printed
    text:   text before loading, default look: Loading: [------    ] 60%

    this loadingbar will load from 1 - 100%, it will have [----   ]
    and a text displaying what "text" is set to

    this function will exit with two new lines

    in case you wonder loadLineDSEL is not for Disel, it is for
    "Loadingbar Line Download Style Enter Line" dont really know what E is for yet
    """

    #extras:
    t = ""
    space = "                   "
    procent = 1
    prev = 0

    #loadingbar loop
    for x in range(100):
        #setting everything
        procent = x

        #this is set only when to aply more "###" to loadingbar line
        if prev == 0:
            prev = x
        elif (x - prev) == 5:
            t = t + "-"
            space = (space + "\b")
            
            prev = x

        line = (t + space)

        #printing the line and waiting for "sleep" amount of seconds
        print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + f"{procent}%", end="\r")
        time.sleep(sleep)
    
    #end
    print(Colors["BOLD"] + text, Colors["FAIL"] + f"[{line}]", Colors["ENDC"] + "100%\n\n")




"""this part is for other than spinning wheels and loadingbars, this is for figures"""




"""this part is for other things, like if you make a terminal and want to get ip"""