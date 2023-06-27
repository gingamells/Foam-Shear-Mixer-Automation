#####Library Imports
import time
import board
import sys
import random
import math
import displayio
import adafruit_ssd1327
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut

#####Board Initialization

#Display Initializaation
i2c = board.I2C() #uses board.SCL and board.SDA
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
display = adafruit_ssd1327.SSD1327(display_bus, width=128, height=128)
bitmap = displayio.Bitmap(128,128,2)

#####Global Variables
cylColor = ["BLUE", "GREEN", "YELLOW", "RED"]
cycleCount = 0
cylVol = 100

bCyl = 0
gCyl = 0
yCyl = 0
rCyl = 0

#####Display Setup
font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
dispText = "AutoFoam!"
bootArea= label.Label(font,text=dispText,color=0xFFFFFF)
bootArea.x = 0
bootArea.y = 64
display.show(bootArea)

dispGroup = displayio.Group()

cancelGroup = displayio.Group()
termPrompt1 = label.Label(font,text="Run",color=0xFFFFFF)
termPrompt1.x = 0
termPrompt1.y = 63
termPrompt2 = label.Label(font,text="Terminated",color=0xFFFFFF)
termPrompt2.x = 0
termPrompt2.y = 88
cancelGroup.append(termPrompt1)
cancelGroup.append(termPrompt2)

pausePrompt = label.Label(font=bitmap_font.load_font("fonts/Junction-regular-24.bdf"),text="PAUSE",color=0xFFFFFF)
pausePrompt.x = 0
pausePrompt.y = 64

#####Pin Assignments

#Cycle count selection dial
dial = AnalogIn(board.A0)
#Buttons and Lights
gb = DigitalInOut(board.D0)
gl = DigitalInOut(board.D1)
yb = DigitalInOut(board.D2)
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

#Buttons and Lights
gb.direction = Direction.INPUT
gb.pull = Pull.UP
gl.direction = Direction.OUTPUT
yb.direction = Direction.INPUT
yb.pull = Pull.UP
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
    textPrompta = label.Label(font,text="Initializing",color=0XFFFFFF)
    textPrompta.x = 0
    textPrompta.y = 15
    display.show(textPrompta)

    gl.value = True
    yl.value = True
    rl.value = True
    AllOpen()
    time.sleep(1)
    gl.value = False
    yl.value = False
    rl.value = False
    time.sleep(1)
    return

def SysSetup():                                     #uses prompts on attached display to ask whether or not a cylinder is full or partially filled. Also determines total cycle count
    textPrompt = label.Label(font,text="Cycle Setup",color=0XFFFFFF)
    textPrompt.x = 0
    textPrompt.y = 15
    dispGroup.append(textPrompt)
    display.show(dispGroup)

    cylBGColor = displayio.Palette(1)
    cylBGColor[0]=0xFFFFFF
    cylBG = displayio.TileGrid(displayio.Bitmap(128,72,2),pixel_shader=cylBGColor,x=0,y=59)
    dispGroup.append(cylBG)

    bCylName = label.Label(font,text="Blue",color=0x000000)
    bCylName.x = 0
    bCylName.y = 68
    dispGroup.append(bCylName)
    gCylName = label.Label(font,text="Green",color=0X000000)
    gCylName.x = 0
    gCylName.y = 85
    dispGroup.append(gCylName)
    yCylName = label.Label(font,text="Yellow",color=0X000000)
    yCylName.x = 0
    yCylName.y = 102
    dispGroup.append(yCylName)
    rCylName = label.Label(font,text="Red",color=0X000000)
    rCylName.x = 0
    rCylName.y = 119
    dispGroup.append(rCylName)
    display.show(dispGroup)

    cylPrompt = label.Label(font,text="",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup.append(cylPrompt)

    #print("Set status of BLUE cylinder.")
    cylPrompt = label.Label(font,text="Blue Status",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup[6] = cylPrompt
    display.show(dispGroup)
    tmp = False
    while tmp == False:
        gl.value = True
        yl.value = True
        rl.value = True
        if gb.value == False:
            bStatus = label.Label(font,text="F",color=0X000000)
            bStatus.x = 115
            bStatus.y = 68

            bCyl = 2
            tmp = True
            yl.value = not yb.value
            rl.value = not rb.value
        elif yb.value == False:
            bStatus = label.Label(font,text="P",color=0X000000)
            bStatus.x = 115
            bStatus.y = 68

            bCyl = 1
            tmp = True
            gl.value = not gb.value
            rl.value = not rb.value
        elif rb.value == False:
            bStatus = label.Label(font,text="E",color=0X000000)
            bStatus.x = 115
            bStatus.y = 68

            bCyl = 0
            tmp = True
            yl.value = not yb.value
            gl.value = not gb.value
    dispGroup.append(bStatus)
    display.show(dispGroup)
    time.sleep(1)

    #print("Set status of GREEN cylinder.")
    cylPrompt = label.Label(font,text="Green Status",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup[6] = cylPrompt
    display.show(dispGroup)
    tmp = False
    while tmp == False:
        gl.value = True
        yl.value = True
        rl.value = True
        if gb.value == False:
            gStatus = label.Label(font,text="F",color=0X000000)
            gStatus.x = 115
            gStatus.y = 85

            gCyl = 2
            tmp = True
            yl.value = not yb.value
            rl.value = not rb.value
        elif yb.value == False:
            gStatus = label.Label(font,text="P",color=0X000000)
            gStatus.x = 115
            gStatus.y = 85

            gCyl = 1
            tmp = True
            gl.value = not gb.value
            rl.value = not rb.value
        elif rb.value == False:
            gStatus = label.Label(font,text="E",color=0X000000)
            gStatus.x = 115
            gStatus.y = 85

            gCyl = 0
            tmp = True
            yl.value = not yb.value
            gl.value = not gb.value
    dispGroup.append(gStatus)
    display.show(dispGroup)
    time.sleep(1)

    #print("Set status of YELLOW cylinder.")
    cylPrompt = label.Label(font,text="Yellow Status",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup[6] = cylPrompt
    display.show(dispGroup)
    tmp = False
    while tmp == False:
        gl.value = True
        yl.value = True
        rl.value = True
        if gb.value == False:
            yStatus = label.Label(font,text="F",color=0X000000)
            yStatus.x = 115
            yStatus.y = 102

            yCyl = 2
            tmp = True
            yl.value = not yb.value
            rl.value = not rb.value
        elif yb.value == False:
            yStatus = label.Label(font,text="P",color=0X000000)
            yStatus.x = 115
            yStatus.y = 102

            yCyl = 1
            tmp = True
            gl.value = not gb.value
            rl.value = not rb.value
        elif rb.value == False:
            yStatus = label.Label(font,text="E",color=0X000000)
            yStatus.x = 115
            yStatus.y = 102

            yCyl = 0
            tmp = True
            yl.value = not yb.value
            gl.value = not gb.value
    dispGroup.append(yStatus)
    display.show(dispGroup)
    time.sleep(1)

    #print("Set status of RED cylinder.")
    cylPrompt = label.Label(font,text="Red Status",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup[6] = cylPrompt
    display.show(dispGroup)
    tmp = False
    while tmp == False:
        gl.value = True
        yl.value = True
        rl.value = True
        if gb.value == False:
            rStatus = label.Label(font,text="F",color=0X000000)
            rStatus.x = 115
            rStatus.y = 119

            rCyl = 2
            tmp = True
            yl.value = not yb.value
            rl.value = not rb.value
        elif yb.value == False:
            rStatus = label.Label(font,text="P",color=0X000000)
            rStatus.x = 115
            rStatus.y = 119

            rCyl = 1
            tmp = True
            gl.value = not gb.value
            rl.value = not rb.value
        elif rb.value == False:
            rStatus = label.Label(font,text="E",color=0X000000)
            rStatus.x = 115
            rStatus.y = 119

            rCyl = 0
            tmp = True
            yl.value = not yb.value
            gl.value = not gb.value
    dispGroup.append(rStatus)
    display.show(dispGroup)
    time.sleep(1)

    if bCyl==0 and gCyl==0 and yCyl==0 and rCyl==0:
        print("All cylinders empty! Terminating program!")
        EStop()

    gl.value = not gb.value
    yl.value = not yb.value
    rl.value = not rb.value
    time.sleep(1)

    #print("Please use the dial to select the number of cyles to automate.")
    cylPrompt = label.Label(font,text="Cycles:",color=0XFFFFFF)
    cylPrompt.x = 0
    cylPrompt.y = 51
    dispGroup[6] = cylPrompt
    display.show(dispGroup)

    cycleNum = label.Label(font,text="0",color=0XFFFFFF)
    cycleNum.x = 95
    cycleNum.y = 51
    dispGroup.append(cycleNum)
    display.show(dispGroup)

    tmp = False
    while tmp == False:
        #print("Number of cycles to automate: ", math.floor(dial.value/655.35))
        totalCycles = math.floor(dial.value/655.35)
        cycleNum = label.Label(font,text=str(totalCycles),color=0XFFFFFF)
        cycleNum.x = 95
        cycleNum.y = 51
        dispGroup[11] = cycleNum
        display.show(dispGroup)

        gl.value = True
        #time.sleep(0.25)
        if gb.value == False:
            totalCycles = math.floor(dial.value/655.35)
            tmp = True
    gl.value = False
    return totalCycles, [bCyl,gCyl,yCyl,rCyl]
    return totalCycles, [bCyl,gCyl,yCyl,rCyl]

def Pause():
    time.sleep(1)
    while yb.value == True:
        #print("System Paused")
        AllClose()
        display.show(pausePrompt)
        yl.value = not yl.value
        time.sleep(0.25)
    display.show(dispGroup)
    return

def SingleCylDrive(cylStatus, cylColor):
    runStatus = label.Label(font,text="Running",color=0XFFFFFF)
    runStatus.x = 0
    runStatus.y = 15
    dispGroup[0] = runStatus
    nullLabel = label.Label(font,text="",color=0XFFFFFF)
    nullLabel.x = 0
    nullLabel.y = 51
    dispGroup[6] = nullLabel
    nullLabela = label.Label(font,text="",color=0XFFFFFF)
    nullLabela.x = 0
    nullLabela.y = 51
    nullLabelb = label.Label(font,text="",color=0XFFFFFF)
    nullLabelb.x = 0
    nullLabelb.y = 51
    if len(dispGroup) <= 14:
        dispGroup.append(nullLabela)
        dispGroup.append(nullLabelb)
    else:
        dispGroup[13] = nullLabela
        dispGroup[14] = nullLabelb
    display.show(dispGroup)

    tmp, partialDrive = False, False
    driveSelect, ventSelect = 5, 5
    while tmp == False:
        rand = random.randint(0,3)
        if cylStatus[rand] != 0:
            driveSelect = rand
            tmp = True
    #print("driveSelect = ", driveSelect)

    for i in range(0,len(cylStatus)):                            #provides index for cylStatus of empty cylinder
        if cylStatus[i] == 0:
            ventSelect = i

    #print("ventSelect = ", ventSelect)

    if cylStatus[driveSelect] != 2:                     #If cylinder is not "FULL" work around
        #print("Partially filled cylinder selected to drive!")
        yl.value = True
        partialDrive = True

    #print(f"Driving {cylColor[driveSelect]} into {cylColor[ventSelect]}.")

    while gb.value == True:                             #temporarily using yb as trigger to complete drive
        if ventSelect == 0:
            bCylVent.value = True
            vPrompt = label.Label(font,text="V",color=0X000000)
            vPrompt.x = 90
            vPrompt.y = 68
            dispGroup[13] = vPrompt
        elif ventSelect == 1:
            gCylVent.value = True
            vPrompt = label.Label(font,text="V",color=0X000000)
            vPrompt.x = 90
            vPrompt.y = 85
            dispGroup[13] = vPrompt
        elif ventSelect == 2:
            yCylVent.value = True
            vPrompt = label.Label(font,text="V",color=0X000000)
            vPrompt.x = 90
            vPrompt.y = 102
            dispGroup[13] = vPrompt
        elif ventSelect == 3:
            rCylVent.value = True
            vPrompt = label.Label(font,text="V",color=0X000000)
            vPrompt.x = 90
            vPrompt.y = 119
            dispGroup[13] = vPrompt
        else:
            EStop()

        if driveSelect == 0:
            bCylDrive.value = True
            dPrompt = label.Label(font,text="D",color=0X000000)
            dPrompt.x = 90
            dPrompt.y = 68
            dispGroup[14] = dPrompt
        elif driveSelect == 1:
            gCylDrive.value = True
            dPrompt = label.Label(font,text="D",color=0X000000)
            dPrompt.x = 90
            dPrompt.y = 85
            dispGroup[14] = dPrompt
        elif driveSelect == 2:
            yCylDrive.value = True
            dPrompt = label.Label(font,text="D",color=0X000000)
            dPrompt.x = 90
            dPrompt.y = 102
            dispGroup[14] = dPrompt
        elif driveSelect == 3:
            rCylDrive.value = True
            dPrompt = label.Label(font,text="D",color=0X000000)
            dPrompt.x = 90
            dPrompt.y = 119
            dispGroup[14] = dPrompt
        else:
            EStop()
        display.show(dispGroup)

        if rb.value == False:
            #CONTINUE RUNNING UNTIL CYL IS FILLED TO PREVENT PARTIAL CYLS
            #EStop()
            return [0,0,0,0]

        if yb.value == False:
            Pause()
            time.sleep(0.25)
        time.sleep(0.25)

    cylStatus[ventSelect] = 2
    if partialDrive == True:
        cylStatus[ventSelect] = 1
    cylStatus[driveSelect] = 0
    yl.value = False
    #print("Cycle Complete!")
    AllClose()
    return cylStatus

def EStop():
    AllClose()
    rl.value = True
    #print("Mixing has terminated!")
    sys.exit(0)                                 #Terminates code and exits run (delete/comment out if code should run and be reactivated with button push)
    return

def Shutdown():

    return

#####Main##################################################################################
#print("\nSystem Startup")
SysStart()
startPrompt = label.Label(font,text="Sys Standby",color=0XFFFFFF)
startPrompt.x = 0
startPrompt.y = 63
display.show(startPrompt)
#print("System Ready for Cycle Setup")
time.sleep(1)

while True:
    dispGroup = displayio.Group()
    gl.value = True
    yl.value = False
    rl.value = False
    while gb.value == True:
        tmpPrompt = label.Label(font,text="Sys Standby",color=0XFFFFFF)
        tmpPrompt.x = 0
        tmpPrompt.y = 63
        display.show(tmpPrompt)
        gl.value = not gl.value
        yl.value = not yl.value
        time.sleep(0.25)

    if gb.value == False:
        gl.value = not gb.value
        rl.value = gb.value
        AllClose()
        time.sleep(0.25)
        totalCycles, cylStatus = SysSetup()
        #print(f"\nSequence set to {totalCycles} cycles.")
        #print(f"Status: Blue: {cylStatus[0]}, Green: {cylStatus[1]}, Yellow: {cylStatus[2]}, Red: {cylStatus[3]}")
        time.sleep(1)
        #print("Ready to Run!")
        while gb.value == True:
            readyPrompt = label.Label(font,text="Sys Ready",color=0xFFFFFF)
            readyPrompt.x = 0
            readyPrompt.y = 15
            dispGroup[0] = readyPrompt
            display.show(dispGroup)

            gl.value = True
            rl.value = False
            time.sleep(0.25)
            gl.value = False
            yl.value = True
            time.sleep(0.25)
            yl.value = False
            rl.value = True
            time.sleep(0.25)
        gl.value = True
        rl.value = False
        yl.value = False

        cylPrompt = label.Label(font,text="1 of ",color=0XFFFFFF)
        cylPrompt.x = 45
        cylPrompt.y = 51
        dispGroup.append(cylPrompt)

        for cycleNum in range(1,totalCycles+1):
            print(f"\nRunning cycle # {cycleNum} with drive code {cylStatus}")
            time.sleep(0.25)
            cylStatus = SingleCylDrive(cylStatus, cylColor)

            cyclePrompt = label.Label(font,text=str(cycleNum+1)+" of ",color=0xFFFFFF)
            cyclePrompt.x = 37
            cyclePrompt.y = 51
            dispGroup[12] = cyclePrompt
            display.show(dispGroup)

            if cylStatus == [0,0,0,0]:
                #print("Cycle Force Termination at Cycle # ",cycleNum)
                AllClose()
                display.show(cancelGroup)
                cycleNum = totalCycles
                dispGroup = displayio.Group()
                rl.value = True
                time.sleep(2)
                break
        #print("Sequence complete!")
        compGroup = displayio.Group()
        compPrompt1 = label.Label(font,text="Sequence",color=0XFFFFFF)
        compPrompt1.x = 0
        compPrompt1.y = 45
        compGroup.append(compPrompt1)
        compPrompt2 = label.Label(font,text="Complete!",color=0XFFFFFF)
        compPrompt2.x = 0
        compPrompt2.y = 69
        compGroup.append(compPrompt2)
        display.show(compGroup)
        time.sleep(5)
