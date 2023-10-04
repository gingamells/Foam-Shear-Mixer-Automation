#Imports
import customtkinter
import tkinter as tk
import pyfirmata
import time
import random

#Variables
cylStatus = [0,0,0,0]
processList = ["Water", "FOAM", "Succor", "TBD"]
processMFCTriggers = [.25, .40, .20, 0]

class cyl_status_frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(3,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.bStat = tk.StringVar()
        self.bStat.set("")
        self.gStat = tk.StringVar()
        self.gStat.set("")
        self.yStat = tk.StringVar()
        self.yStat.set("")
        self.rStat = tk.StringVar()
        self.rStat.set("")
        
        self.bdrive = tk.StringVar()
        self.bdrive.set("")
        self.gdrive = tk.StringVar()
        self.gdrive.set("")
        self.ydrive = tk.StringVar()
        self.ydrive.set("")
        self.rdrive = tk.StringVar()
        self.rdrive.set("")
        
        self.cylB = customtkinter.CTkFrame(self, width=115, height=125, fg_color='blue', corner_radius=10)
        self.cylB.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.cylB.grid_columnconfigure(2, weight=1)
        self.cylB.titleB = customtkinter.CTkLabel(self.cylB, width=105, height=75, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), text="BLUE", text_color="black")
        self.cylB.titleB.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.cylB.labelB = customtkinter.CTkLabel(self.cylB, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.bStat)
        self.cylB.labelB.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.cylB.driveB = customtkinter.CTkLabel(self.cylB, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.bdrive)
        self.cylB.driveB.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
        self.cylG = customtkinter.CTkFrame(self, width=115, height=125, fg_color='green', corner_radius=10)
        self.cylG.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.cylG.grid_columnconfigure(2, weight=1)
        self.cylG.titleG = customtkinter.CTkLabel(self.cylG, width=105, height=75, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), text="GREEN", text_color="black")
        self.cylG.titleG.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.cylG.labelG = customtkinter.CTkLabel(self.cylG, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.gStat)
        self.cylG.labelG.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.cylG.driveG = customtkinter.CTkLabel(self.cylG, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.gdrive)
        self.cylG.driveG.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
        self.cylY = customtkinter.CTkFrame(self, width=115, height=125, fg_color='yellow', corner_radius=10)
        self.cylY.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        self.cylY.grid_columnconfigure(2, weight=1)
        self.cylY.titleY = customtkinter.CTkLabel(self.cylY, width=105, height=75, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), text="Yellow", text_color="black")
        self.cylY.titleY.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.cylY.labelY = customtkinter.CTkLabel(self.cylY, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.yStat)
        self.cylY.labelY.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.cylY.driveY = customtkinter.CTkLabel(self.cylY, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.ydrive)
        self.cylY.driveY.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
        self.cylR = customtkinter.CTkFrame(self, width=115, height=125, fg_color='red', corner_radius=10)
        self.cylR.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
        self.cylR.grid_columnconfigure(2, weight=1)
        self.cylR.titleR = customtkinter.CTkLabel(self.cylR, width=105, height=75, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), text="RED", text_color="black")
        self.cylR.titleR.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.cylR.labelR = customtkinter.CTkLabel(self.cylR, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.rStat)
        self.cylR.labelR.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.cylR.driveR = customtkinter.CTkLabel(self.cylR, width=105, justify='center', fg_color="gray", corner_radius=10, font=("Arial", 16), textvariable=self.rdrive)
        self.cylR.driveR.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')       

class buttons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(0,weight=1)
        
        self.buttonPlay = customtkinter.CTkButton(self, text="PLAY", command=master.play_button_callback, width=75, height=75, fg_color='green', text_color='black', font=("Arial", 18))
        self.buttonPlay.grid(row=0, column=0, padx=5, pady=5, sticky='snew')
        self.buttonPause = customtkinter.CTkButton(self, text="PAUSE", command=master.pause_button_callback, width=75, height=75, fg_color='yellow', text_color='black', font=("Arial", 18))
        self.buttonPause.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')        
        self.buttonStop = customtkinter.CTkButton(self, text="STOP", command=master.stop_button_callback, width=75, height=75, fg_color='red', text_color='white', font=("Arial", 18))
        self.buttonStop.grid(row=0, column=2, padx=5, pady=5, sticky='snew')

class sys_status(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.statusTitle = customtkinter.CTkLabel(self, text="System Status", justify="center", font=("Arial", 18), fg_color='gray', corner_radius=5)
        self.statusTitle.grid(row=0, column=0, padx=5, pady=5,sticky='nsew')
        
        self.statusLabel = customtkinter.CTkLabel(self, justify='center', font=("Arial", 18))
        self.statusLabel.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.statusText = tk.StringVar()
        self.statusText.set("Standby...")
        self.statusLabel.configure(textvariable=self.statusText)
        self.statusLabel.update()
        
class cycle_num(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.cycleLabel = customtkinter.CTkLabel(self, text="Cycle Count", justify="center", font=("Arial", 18), fg_color='gray', corner_radius=5)
        self.cycleLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.totalCycles = 999
        self.currentCycle = 0
        self.cycleText = tk.StringVar()
        self.cycleText.set(str(self.currentCycle)+" of "+str(self.totalCycles))
        
        self.cycleNum = customtkinter.CTkLabel(self, textvariable=self.cycleText, justify='center', font=("Arial", 18))
        self.cycleNum.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
class main_menu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setupLabel = customtkinter.CTkLabel(self, text="Main Menu", justify='center', font=("Arial", 20))
        self.setupLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        self.setupButton = customtkinter.CTkButton(self, text="Cycle Setup", command=master.setup_button_callback, fg_color='blue', corner_radius=5, font=("Arial", 18))
        self.setupButton.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.processButton = customtkinter.CTkButton(self, text="Process Selection", command=master.process_button_callback, fg_color='blue', corner_radius=5, font=("Arial", 18))
        self.processButton.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
        self.readyButton = customtkinter.CTkButton(self, text="Ready to Run", command=master.ready_button_callback, fg_color='blue', corner_radius=5, font=("Arial", 18))
        self.readyButton.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        
class main_setup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.mainSetupLabel = customtkinter.CTkLabel(self, text="Setup Menu", justify='center', font=("Arial", 18))
        self.mainSetupLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=0, sticky='nsew')
        
        self.bFrame = customtkinter.CTkFrame(self, fg_color='blue')
        self.bFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.bFrame.grid_columnconfigure(0, weight=1)
        self.bFrame.grid_rowconfigure(1, weight=1)
        self.bFrame.bLabel = customtkinter.CTkLabel(self.bFrame, text="BLUE", height=30, fg_color='gray', text_color="black", corner_radius=10, font=("Arial", 18))
        self.bFrame.bLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.bFrame.bOption = customtkinter.CTkOptionMenu(self.bFrame, values=["", "Full","Partial", "Empty"], command=master.bOption_callback, width=105, height=30, font=("Arial", 16))
        self.bFrame.bOption.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.gFrame = customtkinter.CTkFrame(self, fg_color='green')
        self.gFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        self.gFrame.grid_columnconfigure(0, weight=1)
        self.gFrame.grid_rowconfigure(1, weight=1)
        self.gFrame.gLabel = customtkinter.CTkLabel(self.gFrame, text="GREEN", height=30, fg_color='gray', text_color="black", corner_radius=10, font=("Arial", 18))
        self.gFrame.gLabel.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.gFrame.gOption = customtkinter.CTkOptionMenu(self.gFrame, values=["", "Full","Partial", "Empty"], command=master.gOption_callback, width=105, height=30, font=("Arial", 16))
        self.gFrame.gOption.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
        self.yFrame = customtkinter.CTkFrame(self, fg_color='yellow')
        self.yFrame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        self.yFrame.grid_columnconfigure(0, weight=1)
        self.yFrame.grid_rowconfigure(1, weight=1)
        self.yFrame.yLabel = customtkinter.CTkLabel(self.yFrame, text="YELLOW", height=30, fg_color='gray', text_color="black", corner_radius=10, font=("Arial", 18))
        self.yFrame.yLabel.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        self.yFrame.yOption = customtkinter.CTkOptionMenu(self.yFrame, values=["", "Full","Partial", "Empty"], command=master.yOption_callback, width=105, height=30, font=("Arial", 16))
        self.yFrame.yOption.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        
        self.rFrame = customtkinter.CTkFrame(self, fg_color='red')
        self.rFrame.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')
        self.rFrame.grid_columnconfigure(0, weight=1)
        self.rFrame.grid_rowconfigure(1, weight=1)
        self.rFrame.rLabel = customtkinter.CTkLabel(self.rFrame, text="RED", height=30, fg_color='gray', text_color="black", corner_radius=10, font=("Arial", 18))
        self.rFrame.rLabel.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
        self.rFrame.rOption = customtkinter.CTkOptionMenu(self.rFrame, values=["", "Full","Partial", "Empty"], command=master.rOption_callback, width=105, height=30, font=("Arial", 16))
        self.rFrame.rOption.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')
        
        self.cycleFrame = customtkinter.CTkFrame(self, fg_color="gray")
        self.cycleFrame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        self.cycleFrame.columnconfigure(3, weight=1)
        self.cycleFrame.rowconfigure(1, weight=1)
        self.cycleFrame.cycleLabel = customtkinter.CTkLabel(self.cycleFrame, text="Number of Cycles", justify='center', font=("Arial", 18))
        self.cycleFrame.cycleLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=0, sticky='nsew')
        self.cycleNumLabel = tk.StringVar()
        self.cycleNumLabel.set("")
        self.cycleFrame.cycleNumLabel = customtkinter.CTkLabel(self.cycleFrame, textvariable=self.cycleNumLabel, fg_color="black", text_color='white', corner_radius=5, width=45)
        self.cycleFrame.cycleNumLabel.grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
        self.cycleFrame.cycleNum = customtkinter.CTkSlider(self.cycleFrame, from_=0, to=250, command=master.cycleSlider_callback, progress_color='blue')
        self.cycleFrame.cycleNum.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        self.setupConfirm = customtkinter.CTkButton(self, text="Confirm Setup", command=master.setupConfirm_callback, fg_color='blue', corner_radius=5, font=("Arial", 18))
        self.setupConfirm.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
class main_run(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self.mainRunLabel = customtkinter.CTkLabel(self, text="Run Menu", justify='center', font=("Arial", 18))
        self.mainRunLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        
        self.ardStatus = customtkinter.CTkFrame(self, fg_color='gray')
        self.ardStatus.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.ardStatus.rowconfigure(1, weight=1)
        self.ardStatus.ardTitle = customtkinter.CTkLabel(self.ardStatus, text="Arduino  Status", fg_color='cyan', height=50, text_color='black', font=("Arial", 18), corner_radius=5)
        self.ardStatus.ardTitle.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.ardConStatus = tk.StringVar()
        self.ardConStatus.set("Connected")
        self.ardStatus.ardCon = customtkinter.CTkLabel(self.ardStatus, textvariable=self.ardConStatus, text_color='black', font=("Arial", 16))
        self.ardStatus.ardCon.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.skipButton = customtkinter.CTkButton(self, text="Skip Cycle", command=master.skipButton_callback, text_color='black', fg_color='orange', corner_radius=5, font=("Arial", 18))
        self.skipButton.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        
        self.mfcFrame = customtkinter.CTkFrame(self, fg_color="grey")
        self.mfcFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        self.mfcFrame.rowconfigure(1, weight=1)
        self.mfcFrame.mfcLabel = customtkinter.CTkLabel(self.mfcFrame, text="MFC Flow Rate", fg_color='cyan', height=50, text_color='black', font=("Arial", 18), corner_radius=5)
        self.mfcFrame.mfcLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.mfcValue = tk.StringVar()
        self.mfcValue.set("MFC Value")                                       
        self.mfcFrame.mfcData = customtkinter.CTkLabel(self.mfcFrame, textvariable=self.mfcValue, text_color='black', font=("Arial", 16))
        self.mfcFrame.mfcData.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.progressFrame = customtkinter.CTkFrame(self, fg_color="grey")
        self.progressFrame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        self.progressFrame.columnconfigure(0, weight=1)
        self.progressFrame.rowconfigure(1, weight=1)
        self.progressFrame.progressLabel = customtkinter.CTkLabel(self.progressFrame, text='Cycle Progress', fg_color='cyan', text_color='black', corner_radius=5, font=("Arial", 18))
        self.progressFrame.progressLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.progressFrame.progressBar = customtkinter.CTkProgressBar(self.progressFrame, corner_radius=5, fg_color='black', progress_color='blue', height=15)
        self.progressFrame.progressBar.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
class main_process(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
               
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.mainProcessLabel = customtkinter.CTkLabel(self, text="Process Selection", justify='center', font=("Arial", 18))
        self.mainProcessLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        
        self.processSelectFrame = customtkinter.CTkFrame(self, fg_color="steelblue")
        self.processSelectFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.processSelectFrame.rowconfigure(0, weight=1)
        self.processSelectFrame.columnconfigure(1, weight=1)
        self.processSelectFrame.processSelectLabel = customtkinter.CTkLabel(self.processSelectFrame, text="Select a process:", text_color="white", corner_radius=5, font=("Arial", 18))
        self.processSelectFrame.processSelectLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.processSelectFrame.processSelectDropdown = customtkinter.CTkOptionMenu(self.processSelectFrame, values=processList, command=master.processSelect_callback, font=("Arial", 18))
        self.processSelectFrame.processSelectDropdown.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        self.processConfirm = customtkinter.CTkButton(self, command=master.processSelectConfirm_callback, text='Confirm Process Selection', text_color='white', corner_radius=5, font=("Arial", 18), fg_color='blue')
        self.processConfirm.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        
class main_ready(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        
                
class process(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)
        
        self.processTitle = customtkinter.CTkLabel(self, text="Process Selection", justify="center", font=("Arial", 18), fg_color='gray', corner_radius=5)
        self.processTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        
        self.processText = tk.StringVar()
        self.processText.set("Process")
        self.processLabel = customtkinter.CTkLabel(self, textvariable=self.processText, justify="center", font=("Arial", 18), fg_color='darkslategray', text_color='white', width=125, corner_radius=5)
        self.processLabel.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.triggerValue = tk.StringVar()
        self.triggerValue.set("Trigger")    
        self.triggerLabel = customtkinter.CTkLabel(self, textvariable=self.triggerValue, justify='center', font=("Arial", 18), fg_color='darkslategray', text_color='white', corner_radius=5)
        self.triggerLabel.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
class stopPrompt(customtkinter.CTkToplevel)        :
    def __init__(self, master):
        super().__init__(master)
        
        customtkinter.set_appearance_mode('dark')
        self.title("Process Stopped")
        self.geometry("300x150")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.stopLabel = customtkinter.CTkLabel(self, text="Stop Button Pressed!", font=("Arial", 25), fg_color='red', text_color="black", corner_radius=5, height=70)
        self.stopLabel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.termLabel = customtkinter.CTkLabel(self, text="Run terminated!", font=("Arial", 25), fg_color='red', text_color='black', corner_radius=5)
        self.termLabel.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.AFF = autoFoamFunctions(self)
        self.AFF.initialize()
        
        customtkinter.set_appearance_mode('dark')
        self.title("AutoFOAM")
        self.geometry("800x480")
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(3,weight=1)
        
        self.cylStatusFrame = cyl_status_frame(self)
        self.cylStatusFrame.grid(row=0,rowspan=2, column=0, padx=5, pady=5, sticky="nsew")
        
        self.buttonFrame = buttons(self)
        self.buttonFrame.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        
        self.sysStatusFrame = sys_status(self)
        self.sysStatusFrame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        
        self.cycleNumFrame = cycle_num(self)
        self.cycleNumFrame.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')
        
        self.mainMenuFrame= main_menu(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        
        self.processFrame = process(self)
        self.processFrame.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')
        
        self.stopWindow = None
        self.setupError = None
        self.selectionError = None
        self.readyError = None
        
    def play_button_callback(self):
        print("Play button pressed")
        self.sysStatusFrame.statusText.set("Running...")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        print(self.sysStatusFrame.statusText.get())
        
        print("current cycle: ", self.cycleNumFrame.currentCycle)
        print("total cycles: ", self.cycleNumFrame.totalCycles)
        global cylStatus
        
        while int(self.cycleNumFrame.currentCycle) < int(self.cycleNumFrame.totalCycles):
            self.mainMenuFrame.mfcValue.set(round(float(self.AFF.mfc.read()),2))
            self.mainMenuFrame.progressFrame.progressBar.set(float(self.processFrame.triggerValue.get())/(self.AFF.mfc.read()+1))
            self.mainMenuFrame.update()     
            
            self.cycleNumFrame.currentCycle += 1
            self.cycleNumFrame.cycleText.set(str(self.cycleNumFrame.currentCycle)+" of "+str(self.cycleNumFrame.totalCycles))
            self.cycleNumFrame.update()
            
            cylStatus = self.AFF.CylDrive(cylStatus, float(self.processFrame.triggerValue.get()))

            print("Cycle: ", self.cycleNumFrame.currentCycle)
        
    def pause_button_callback(self):
        print("Pause button pressed")
        self.sysStatusFrame.statusText.set("Paused...")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        self.AFF.AllClose()
        

            
        time.sleep(1)

    def stop_button_callback(self):
        print("Stop button pressed")
        self.sysStatusFrame.statusText.set("Stopped...")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        if self.stopWindow is None or not self.stopWindow.winfo_exists():
            self.stopWindow = stopPrompt(self)
        else:
            self.stopWindow.focus()
        
        self.AFF.running = False         
        self.AFF.AllClose()
        self.cycleNumFrame.currentCycle = self.cycleNumFrame.totalCycles
        self.cycleNumFrame.update()
        
        self.mainMenuFrame = main_menu(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()
        
    def setup_button_callback(self):
        print("Setup button pressed")
        
        self.sysStatusFrame.statusText.set("Cycle Setup")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        self.mainMenuFrame = main_setup(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()
        
    def setupConfirm_callback(self):
        print("Setup confirmed")
        self.cycleNumFrame.totalCycles = self.mainMenuFrame.cycleNumLabel.get()
        self.cycleNumFrame.cycleText.set(str(self.cycleNumFrame.currentCycle)+" of "+str(self.cycleNumFrame.totalCycles))
        
        self.sysStatusFrame.statusText.set("Setup Complete")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        self.mainMenuFrame = main_menu(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()
        
        if self.cylStatusFrame.bStat.get() == "Full":
            cylStatus[0] = 2
        elif self.cylStatusFrame.bStat.get() == "Partial":
            cylStatus[0] = 1
        else:
            cylStatus[0] = 0
            
        if self.cylStatusFrame.gStat.get() == "Full":
            cylStatus[1] = 2
        elif self.cylStatusFrame.gStat.get() == "Partial":
            cylStatus[1] = 1
        else:
            cylStatus[1] = 0
            
        if self.cylStatusFrame.yStat.get() == "Full":
            cylStatus[2] = 2
        elif self.cylStatusFrame.yStat.get() == "Partial":
            cylStatus[2] = 1
        else:
            cylStatus[2] = 0
            
        if self.cylStatusFrame.rStat.get() == "Full":
            cylStatus[3] = 2
        elif self.cylStatusFrame.rStat.get() == "Partial":
            cylStatus[3] = 1
        else:
            cylStatus[3] = 0
            
        print(cylStatus)
        
    def process_button_callback(self):
        print("Process button pressed")
        self.mainMenuFrame = main_process(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()
        
        self.sysStatusFrame.statusText.set("Process Selection")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
    def ready_button_callback(self):
        print("Ready button pressed")
        
        self.sysStatusFrame.statusText.set("Ready...")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        self.mainMenuFrame = main_run(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()
        
    def bOption_callback(self, bChoice):
        print("Blue status selected")
        self.cylStatusFrame.bStat.set(str(bChoice))
        
    def gOption_callback(self, gChoice):
        print("Green status selected")
        self.cylStatusFrame.gStat.set(str(gChoice))
        
    def yOption_callback(self, yChoice):
        print("Yellow status selected")
        self.cylStatusFrame.yStat.set(str(yChoice))
        
    def rOption_callback(self,rChoice):
        print("Red status selected")
        self.cylStatusFrame.rStat.set(str(rChoice))
    
    def cycleSlider_callback(self, cycleChoice):
        self.mainMenuFrame.cycleNumLabel.set(str(round(cycleChoice)))
        
    def skipButton_callback(self):
        print("Skip Cycle Button Pressed")
        
        #Functionality Test
        self.AFF.AllClose()
        self.AFF.running = False
        time.sleep(1)
        #self.AFF.running = False
        
        
    def processSelect_callback(self, processChoice):
        print("Process selected")
        self.processFrame.processText.set(str(processChoice))
        self.processFrame.triggerValue.set(str(processMFCTriggers[processList.index(processChoice)]))

    def processSelectConfirm_callback(self):
        print("Process confirmed")
        
        self.sysStatusFrame.statusText.set("Process Selected")
        self.sysStatusFrame.statusLabel.configure(textvariable=self.sysStatusFrame.statusText)
        self.sysStatusFrame.statusLabel.update()
        
        self.mainMenuFrame = main_menu(self)
        self.mainMenuFrame.grid(row=2, rowspan=2, column=0, padx=5, pady=5, sticky='nsew')
        self.mainMenuFrame.update()

class autoFoamFunctions():
    def __init__(self, master):
        super().__init__()
        
    def initialize(self):
        board = pyfirmata.Arduino('/dev/ttyACM0')
        print("Communication successfully started!")

        #####Pin Assignments
        it = pyfirmata.util.Iterator(board)
        it.start()

        #Solenoids
        self.bCylDrive = board.digital[2]
        self.bCylVent = board.digital[3]
        self.gCylDrive = board.digital[4]
        self.gCylVent = board.digital[5]
        self.yCylDrive = board.digital[6]
        self.yCylVent = board.digital[7]
        self.rCylDrive = board.digital[8]
        self.rCylVent = board.digital[9]

        #####Pin Inputs/Outputs
        #MFC
        self.mfc = board.get_pin("a:1:i")
        
    def AllOpen(self):
        self.bCylDrive.write(1)
        self.bCylVent.write(1)
        self.gCylDrive.write(1)
        self.gCylVent.write(1)
        self.yCylDrive.write(1)
        self.yCylVent.write(1)
        self.rCylDrive.write(1)
        self.rCylVent.write(1)
        
    def AllClose(self):
        self.bCylDrive.write(0)
        self.bCylVent.write(0)
        self.gCylDrive.write(0)
        self.gCylVent.write(0)
        self.yCylDrive.write(0)
        self.yCylVent.write(0)
        self.rCylDrive.write(0)
        self.rCylVent.write(0)
        
    def CylDrive(self, cylStatusin, mfcTrigger):
        tmp, partialDrive = False, False
        driveSelect, ventSelect = 5, 5
        while tmp == False:
            rand = random.randint(0,3)
            if cylStatusin[rand] != 0:
                driveSelect = rand
                tmp = True

        for i in range(0,len(cylStatusin)):                            #provides index for cylStatus of empty cylinder
            if cylStatus[i] == 0:
                ventSelect = i

        if cylStatusin[driveSelect] != 2:                     #If cylinder is not "FULL" work around
            #print("Partially filled cylinder selected to drive!")
            ###################################################### INDICATOR FOR PARTIAL DRIVE
            partialDrive = True

        app.cylStatusFrame.cylB.driveB.configure(fg_color="gray")
        app.cylStatusFrame.cylG.driveG.configure(fg_color="gray")
        app.cylStatusFrame.cylY.driveY.configure(fg_color="gray")
        app.cylStatusFrame.cylR.driveR.configure(fg_color="gray")
        app.cylStatusFrame.bdrive.set("")
        app.cylStatusFrame.gdrive.set("")
        app.cylStatusFrame.ydrive.set("")
        app.cylStatusFrame.rdrive.set("")

        #time.sleep(3) #wait 3 seconds for system to adjust after switching to new cylinder to prevent instantly triggering next cylinder
        self.running = True

        while self.running == True:
            
            #print("MFC Value: ", self.mfc.read()*100000)
            
            if driveSelect == 0:
                self.bCylDrive.write(1)
                app.cylStatusFrame.bdrive.set("Driving")
                if partialDrive==False:
                    app.cylStatusFrame.cylB.driveB.configure(fg_color="green")
                else:
                    app.cylStatusFrame.cylB.driveB.configure(fg_color="yellow")
            elif driveSelect == 1:
                self.gCylDrive.write(1)
                app.cylStatusFrame.gdrive.set("Driving")
                if partialDrive==False:
                    app.cylStatusFrame.cylG.driveG.configure(fg_color="green")
                else:
                    app.cylStatusFrame.cylG.driveG.configure(fg_color="yellow")
            elif driveSelect == 2:
                self.yCylDrive.write(1)
                app.cylStatusFrame.ydrive.set("Driving")
                if partialDrive==False:
                    app.cylStatusFrame.cylY.driveY.configure(fg_color="green")
                else:
                    app.cylStatusFrame.cylY.driveY.configure(fg_color="yellow")
            elif driveSelect == 3:
                self.rCylDrive.write(1)
                app.cylStatusFrame.rdrive.set("Driving")
                if partialDrive==False:
                    app.cylStatusFrame.cylR.driveR.configure(fg_color="green")
                else:
                    app.cylStatusFrame.cylR.driveR.configure(fg_color="yellow")
            else:
                self.EStop()

            if ventSelect == 0:
                self.bCylVent.write(1)
                app.cylStatusFrame.bdrive.set("Venting")
                app.cylStatusFrame.cylB.driveB.configure(fg_color="red")
            elif ventSelect == 1:
                self.gCylVent.write(1)
                app.cylStatusFrame.gdrive.set("Venting")
                app.cylStatusFrame.cylG.driveG.configure(fg_color="red")
            elif ventSelect == 2:
                self.yCylVent.write(1)
                app.cylStatusFrame.ydrive.set("Venting")
                app.cylStatusFrame.cylY.driveY.configure(fg_color="red")
            elif ventSelect == 3:
                self.rCylVent.write(1)
                app.cylStatusFrame.rdrive.set("Venting")
                app.cylStatusFrame.cylR.driveR.configure(fg_color="red")
            else:
                self.EStop()
            app.cylStatusFrame.update()
            print("MFC Value:", self.mfc.read())
            print("MFC Trigger:", mfcTrigger)
            time.sleep(2)
            
            if self.mfc.read() < mfcTrigger:           #remove the number when using actual MFC
                self.running = False
                
            app.mainMenuFrame.mfcValue.set(round(float(self.mfc.read()*100000),2))               
            app.mainMenuFrame.progressFrame.progressBar.set(float(app.processFrame.triggerValue.get())/(self.mfc.read()+1))
            app.mainMenuFrame.update()  
                
            #Frame updates
        if ventSelect == 0:
            app.cylStatusFrame.bStat.set("Full")
        elif ventSelect == 1:
            app.cylStatusFrame.gStat.set("Full")
        elif ventSelect == 2:
            app.cylStatusFrame.yStat.set("Full")
        elif ventSelect == 3:
            app.cylStatusFrame.rStat.set("Full")
        else:
            self.Estop()
            
        if driveSelect == 0:
            app.cylStatusFrame.bStat.set("Empty")
        elif driveSelect == 1:
            app.cylStatusFrame.gStat.set("Empty")
        elif driveSelect == 2:
            app.cylStatusFrame.yStat.set("Empty")
        elif driveSelect == 3:
            app.cylStatusFrame.rStat.set("Empty")
        else:
            self.EStop()
            
        cylStatusin[ventSelect] = 2
        if partialDrive == True:
            cylStatusin[ventSelect] = 1
        cylStatusin[driveSelect] = 0
        

        
        #print("Cycle Complete!")
        self.AllClose()
        return cylStatusin

    def EStop(self):
        print("ESTOP PRESSED")

app = App()
app.mainloop()