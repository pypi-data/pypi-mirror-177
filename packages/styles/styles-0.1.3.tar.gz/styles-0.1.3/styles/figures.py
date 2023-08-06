"""
this simple program can make terminal figure output.
Note: that this does not make an app or ui with the figure in it
"""
#imports:
import time



#this is a simple lite program to make a line
def line(flush=bool(True), times=int(15), delay=float(0.1)):
    """
    this will make a simple line, just like a loadingbar, but diffrent

    flush:  just like print, this will look cooler
    times:  how many times "-" to be printed
    delay:  this will make a delay before every print, needs flush=True

    this will make something like this: ------------------
    this uses the default color, so there is no color change
    """

    for x in range(times):
        print("-", sep="", end="", flush=flush)
        time.sleep(delay)