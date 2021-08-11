import serial
from time import sleep

#be sure to "Run Cont." on the plotter before starting this script!!
## Version 2  Hopefully Optimized to not crash plotter
##Made by Spencer Nelson @ NelsonIT.TX@gmail.com

speed = 0.1 #seconds between each PU command - affects small commands more

f = open("inkcut.hpgl","r") #point this at your hpgl file
file = f.read()
f.close()
commands = file.split(";")

Queue = ""
coords = 0 #number of individual parts to any given command
safety = 1200 #limit to size of command
safe = True

with serial.Serial() as ser: #opens serial connection
    ser.baudrate = 9600 #default for Gerber GS750
    ser.port = 'COM3' #set this to your output port
    ser.open()

# Iterates through hpgl file looking for lines that are likely to overwhelm the plotter

    for command in commands:
        if "PU" in command:
            coords = 0
        coords += 1
        
        if coords >= safety:
            print("Safety exceeded, cut long paths in file and try again.")
            safe = False    #If you want to disable the check, comment these two lines
            break           #

    if safe == True:
        print("File is safe, cutting.")
        for command in commands:
            if "PU" in command:
                print(Queue)
                ser.write(str.encode(Queue))
                print("coords: " + str(coords))

                #This section helps keep from wasting time.
                #It's important that you can hear the plotter wait occasionally.
                #There's probably a more clever way of doing this, but I can't be bothered.

                if coords <= 4:
                    speed = 0.25
                elif coords == 5:#usually large squares
                    speed = 1
                elif coords <= 10:
                    speed = 0.30
                elif coords <= 20:
                    speed = 0.25
                elif coords <= 100:
                    speed = 0.15
                elif coords <= 150:
                    speed = 0.1
                else:
                    speed = 0.085
                
        
                wait = round(coords*speed,2) #actually wait
                print("speed: " + str(speed))
                print("sleeping for " + str(wait) + " seconds")
                sleep(wait)
            
                Queue = ""
                coords = 0
                
            Queue += command + ";"
            coords += 1
            
        print(Queue)
        ser.write(str.encode(Queue))#sends last line of file
        print("Finished")      
