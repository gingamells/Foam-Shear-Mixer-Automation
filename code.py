#####Library Imports
import time
import board
import sys
import random
import displayio
import ssd1327

from select import poll
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut

#####Board Initialization
#Display Initializaation
#i2c = board.I2C() #uses board.SCL and board.SDA
#display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
#display = ssd1327.SSD1327(display_bus, width=128, height=128)


#####Global Variables
cylColor = ["blue", "green", "yellow", "red"]
cycleCount = 0
cylVol = 100

#####Pin Assignments
#Vent Flow Indicator
vfi = DigitalInOut(board.D0)
#Flow Percentage Tracker
flowPer = AnalogIn(board.A0)
#Buttons and Lights
gb = DigitalInOut(board.D1)
gl = DigitalInOut(board.D2)
yl = DigitalInOut(board.D3)
rb = DigitalInOut(board.D4)
rl = DigitalInOut(board.D5)
#Solenoids
bCylDrive = DigitalInOut(board.D6)
bCylVent = DigitalInOut(board.D7)
gCylDrive = DigitalInOut(board.D8)
gCylVent = DigitalInOut(board.D9)
yCylDrive = DigitalInOut(board.D10)
yCylVent = DigitalInOut(board.D11)
rCylDrive = DigitalInOut(board.D12)
rCylVent = DigitalInOut(board.D13)

#####Pin Inputs/Outputs
#Vent Flow Inidicator
vfi.direction = Direction.INPUT
vfi.pull = Pull.UP                                      #temporary use of button to trigger next stage
#Buttons and Lights
gb.direction = Direction.INPUT
gb.pull = Pull.UP
gl.direction = Direction.OUTPUT
yl.direction = Direction.OUTPUT
rb.direction = Direction.INPUT
rb.pull = Pull.UP
rl.direction = Direction.OUTPUT
#Solenoids
bCylDrive.direction = Direction.OUTPUT
bCylVent.direction = Direction.OUTPUT
gCylDrive.direction = Direction.OUTPUT
gCylVent.direction = Direction.OUTPUT
yCylDrive.direction = Direction.OUTPUT
yCylVent.direction = Direction.OUTPUT
rCylDrive.direction = Direction.OUTPUT
rCylVent.direction = Direction.OUTPUT

#Cylinder Status
bCylFull = False
gCylFull = False
yCylFull = False
rCylFull = False

#####Definitions
def AllOpen():
    bCylDrive.value = True
    bCylVent.value = True
    gCylDrive.value = True
    gCylVent.value = True
    yCylDrive.value = True
    yCylVent.value = True
    rCylDrive.value = True
    rCylVent.value = True

def AllClose():
    bCylDrive.value = False
    bCylVent.value = False
    gCylDrive.value = False
    gCylVent.value = False
    yCylDrive.value = False
    yCylVent.value = False
    rCylDrive.value = False
    rCylVent.value = False

def VentClose():
    bCylVent.value = False
    gCylVent.value = False
    yCylVent.value = False
    rCylVent.value = False

def DriveClose():
    bCylDrive.value = False
    gCylDrive.value = False
    yCylDrive.value = False
    rCylDrive.value = False

def SysStart():
    gl.value = True
    yl.value = True
    rl.value = True
    AllOpen()
    time.sleep(1)
    gl.value = False
    yl.value = False
    rl.value = False
    return

def SetCylStatus():                                     #uses prompts on attached display to ask whether or not a cylinder is full or partially filled

    return

def FullCylDrive():
    print("Driving Blue into Green")
    while vfi.value == True:                            #Change logic for actual vent flow indicator
        bCylDrive.value = True
        gCylVent.value = True
        if rb.value == False:
            rl.value = True
            EStop()
            return
    bCylDrive.value = False
    gCylVent.value = False
    time.sleep(0.5)
    print("Driving Green into Yellow")
    while vfi.value == True:                            #Change logic for actual vent flow indicator
        gCylDrive.value = True
        yCylVent.value = True
        if rb.value == False:
            rl.value = True
            EStop()
            return
    gCylDrive.value = False
    yCylVent.value = False
    time.sleep(0.5)
    print("Driving Yellow into Red")
    while vfi.value == True:                            #Change logic for actual vent flow indicator
        yCylDrive.value = True
        rCylVent.value = True
        if rb.value == False:
            rl.value = True
            EStop()
            return
    yCylDrive.value = False
    rCylVent.value = False
    time.sleep(0.5)
    print("Driving Red into Blue")
    while vfi.value == True:                            #Change logic for actual vent flow indicator
        rCylDrive.value = True
        bCylVent.value = True
        if rb.value == False:
            rl.value = True
            EStop()
            return
    rCylDrive.value = False
    bCylVent.value = False
    time.sleep(0.5)
    return

def PartialCylDrive(driveCode, fillCode): #fillCode is an array [w, x, y, z] where each index is percentage to be filled (always =100%)
    print("Partial Drive Initiated")
    if (driveCode[0]+driveCode[1]+driveCode[2]+driveCode[3]) != 100:
        print("Error in Drive Code!")
    elif (fillCode[0]+fillCode[1]+fillCode[2]+fillCode[3]) > 100:
        print("Error in Fill Code!")
    for i in range(len(driveCode)):
        #print("i counter: ", i)
        if driveCode[i] != 0:
            if i==0:
                bCylDrive.value = gb.value
            elif i==1:
                gCylDrive.value = gb.value
            elif i==2:
                yCylDrive.value = gb.value
            elif i==3:
                rCylDrive.value = gb.value
            else:
                return
            for j in range(len(fillCode)):
                if fillCode[j] != 0:
                    if j==0:
                        bCylVent.value = gb.value
                    elif j==1:
                        gCylVent.value = gb.value
                    elif j==2:
                        yCylVent.value = gb.value
                    elif j==3:
                        rCylVent.value = gb.value
                    else:
                        return
                    while flowPer.value/655.35 < fillCode[j]:
                        print("Analog Input: ", flowPer.value/655.35)
                        time.sleep(0.25)
                    while vfi.value == True:
                        print("Reset Flow Dial!!!")
                        time.sleep(1)
                    VentClose()
            DriveClose()
    AllClose()
    return

def TestPartialRun(cycleCount):
    PartialCylDrive([100,0,0,0] , [0,100,0,0])
    cycleCount+=1
    print('Cycle Complete: #', cycleCount)
    PartialCylDrive([0,100,0,0] , [0,0,100,0])
    cycleCount+=1
    print('Cycle Complete: #', cycleCount)
    PartialCylDrive([0,0,100,0] , [0,0,0,100])
    cycleCount+=1
    print('Cycle Complete: #', cycleCount)
    PartialCylDrive([0,0,0,100] , [50,50,0,0])
    cycleCount+=1
    print('Cycle Complete: #', cycleCount)
    return

def EStop():
    AllClose()
    print("Cycle has terminated!")
    sys.exit(0)                                 #Terminates code and exits run (delete/comment out if code should run and be reactivated with button push)
    return

#####Main
print("System Startup")
SysStart()
cycleCount = 0
print("System Ready")

print("Analog input: ", flowPer.value)

while True:
    while gb.value == True:
        gl.value = gb.value
        time.sleep(0.5)
        gl.value = not gb.value
        time.sleep(0.5)
        if rb.value == False:
            rl.value = True
            EStop()

    if gb.value == False:
        gl.value = not gb.value
        rl.value = gb.value
        AllClose()
        time.sleep(0.5)
        FullCylDrive()
        #TestPartialRun(cycleCount)
