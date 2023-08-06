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

    sleep:  time delay before next character is printed
    text:   set the text before loading, by default it has not space

    this time you can not change amount of characters to print
    it will always print "##" 10 times: ####################

    ends with two new lines, and the default color
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