import serial
import serial.tools.list_ports
import csv
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from Tkinter import *

# - PLOTTING SETUP
f = Figure(figsize=(10,5), dpi=100)
a = f.add_subplot(111, axisbg='black')
root = Tk()
root.title("Rhizo Data")
leftSide = Frame(root)
rightSide = Frame(root)
bottomSide = Frame(root)
bottomSide.grid(row=3, column=1, sticky='SE')
leftSide.grid(row=0, column=0, sticky='NW', rowspan=3, padx=10, pady=10)
rightSide.grid(row=0, column=1, sticky='NW', columnspan=3, padx=10, pady=10)


bottomRight = Frame(root)
bottomRight.grid(row=1, column=1, sticky='NW', padx=10, pady=10)

running = True

# - LABELS AND TEXT 
cLabel = Label(rightSide, text="Cube Temperature")
cLabel.grid(row=0, column=0, sticky='W', padx=2, pady=2)
cLog = Text(rightSide, width=5, height=1)
cLog.grid(row=0, column=1, sticky='W', padx=2, pady=2)

wLabel = Label(rightSide, text="Water Temperature")
wLabel.grid(row=1, column=0, sticky='W', padx=2, pady=2)
wLog = Text(rightSide, width=5, height=1)
wLog.grid(row=1, column=1, sticky='W', padx=2, pady=2)

aLabel = Label(rightSide, text="Ambient Temperature")
aLabel.grid(row=2, column=0, sticky='W', padx=2, pady=2)
aLog = Text(rightSide, width=5, height=1)
aLog.grid(row=2, column=1, sticky='W', padx=2, pady=2)

dWCLabel = Label(rightSide, text="Water - Cube Temp")
dWCLabel.grid(row=3, column=0, sticky='W', padx=2, pady=2)
dWCLog = Text(rightSide, width=5, height=1, fg="red")
dWCLog.grid(row=3, column=1, sticky='W', padx=2, pady=2)

secLabel = Label(bottomRight, text="Seconds")
secLabel.grid(row=0, column=0, sticky='W', padx=2, pady=25)
secLog = Text(bottomRight, width=7, height=1)
secLog.grid(row=0, column=1, sticky='W', padx=2, pady=10)

minCL = Label(bottomRight, text='Cube')
minCL.grid(row=2, column=0, sticky='W', padx=2, pady=2)
minWL = Label(bottomRight, text='Water')
minWL.grid(row=3, column=0, sticky='W', padx=2, pady=2)
minAL = Label(bottomRight, text='Amb')
minAL.grid(row=4, column=0, sticky='W', padx=2, pady=2)
wtctL = Label(bottomRight, text='WT-CT')
wtctL.grid(row=5, column=0, sticky='W', padx=2, pady=2)

minLabel = Label(bottomRight, text="Min")
minLabel.grid(row=1, column=1, sticky='W', padx=2, pady=2)
maxLabel = Label(bottomRight, text="Max")
maxLabel.grid(row=1, column=2, sticky='W', padx=2, pady=2)


minCLog = Text(bottomRight, width=7, height=1)
minCLog.grid(row=2, column=1,sticky='W', padx=2, pady=2)
minWLog = Text(bottomRight, width=7, height=1)
minWLog.grid(row=3, column=1,sticky='W', padx=2, pady=2)
minALog = Text(bottomRight, width=7, height=1)
minALog.grid(row=4, column=1,sticky='W', padx=2, pady=2)
minWTCTLog = Text(bottomRight, width=7, height=1)
minWTCTLog.grid(row=5, column=1, sticky='W', padx=2, pady=2)

maxCLog = Text(bottomRight, width=7, height=1)
maxCLog.grid(row=2, column=2,sticky='W', padx=2, pady=2)
maxWLog = Text(bottomRight, width=7, height=1)
maxWLog.grid(row=3, column=2,sticky='W', padx=2, pady=2)
maxALog = Text(bottomRight, width=7, height=1)
maxALog.grid(row=4, column=2,sticky='W', padx=2, pady=2)
maxWTCTLog = Text(bottomRight, width=7, height=1)
maxWTCTLog.grid(row=5, column=2, sticky='W', padx=2, pady=2)


# - LIST SETUP
index = 0
tempC, tempW, tempH, dTempWC = [], [], [], []
tempCL, tempWL, tempHL, xList, dTempWCL = [], [], [], [], []
secList, minList, maxList = [], [], []
dataT = tempCL, tempWL, tempHL

# - SERIAL DATA
arduinoData = serial.Serial('/dev/ttyUSB0', 9600)




'''
# - LIST OF PORTS
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p[0]
'''    

def loadFile():
        # - CHECK SYSTEM AND LOAD THE DATA FILE
        if platform.system() == 'Linux':
            portSource = serial.Serial('/dev/ttyUSB0', 9600)
            fileName = '/home/matthew/ownCloud/Code/dataFile.csv'

            
        else:
            portSource = serial.Serial('/dev/tty.usbserial-AH00ZJZ9', 9600)
            fileName = '/Users/matthewgarsteck/ownCloud/Code/dataFile.csv'

        #print self.portSource
         
        fileData = open(fileName, 'r')
        
        # - CHECK TO SEE IF FILE IS EMPTY
        
        for n in fileData:
            print "This is your data: ", n
            if n != "CubeID":
                print "OK"
                writer = csv.writer(sfileData)
                writer.writerow(["CubeID", "WaterTemp"])
          
            
        with open(fileName, 'wb') as f:
            if fileData == ',' or fileData == "" or fileData ==" ":
                print "OK"
                writer = csv.writer(f)
                writer.writerow(["CubeID", "WaterTemp"])
        f.close()

# - ON OFF BUTTON TO SAVE AND DISPLAY DATA
def resetButton():
    
    tempC, tempW, tempH, secList = [], [], [], []    
    ani = animation.FuncAnimation(f, animate, interval=1000)
    
def saveButton():
    with open("/home/matthew/sketchbook/data.csv", 'wb') as mf:
        writer = csv.writer(mf)
        writer.writerow(["Cube","Water","Ambient",("Seconds: " + str(int(xList[-1])))])
        for tC, tW, tH in zip(dataT[0], dataT[1], dataT[2]):
            writer.writerow([tC, tW, tH])
    mf.close()    



def animate(i):
    
    # - GET THE DATA AND SORT IT
    temp = arduinoData.readline()
    tempC, tempW, tempH = map(float, temp.split(","))
    dTempWC = float(tempW) - float(tempC)
    tempCL.append(float(tempC))
    tempWL.append(float(tempW))
    tempHL.append(float(tempH))
    xList.append(int(len(tempCL)))
    dTempWCL.append(float(dTempWC))
    
    # - CALCULATE MIN AND MAX FOR ANALYSIS
    secList = int(xList[-1])
    minC = min(tempCL)
    minW = min(tempWL)
    maxC = max(tempCL)
    maxW = max(tempWL)
    minA = min(tempHL)
    maxA = max(tempHL)
    
    # - PLOT AND LOG THE DATA
    a.clear()
    a.plot(xList, tempCL, color='green', label='Cube')
    a.plot(xList, tempWL, color='blue', label='Water')
    a.plot(xList, tempHL, color='yellow', label='Ambient')
    a.plot(xList, dTempWCL, color='red', label='WT-CT')
    a.set_ylabel("Temperature (F)", fontsize=10)
    a.set_xlabel("Time (s)")
    
    cLog.delete('0.0', 'end')
    wLog.delete('0.0', 'end')
    aLog.delete('0.0', 'end')
    dWCLog.delete('0.0', 'end')
    
    cLog.insert('0.0', str(tempC))
    wLog.insert('0.0', str(tempW))
    aLog.insert('0.0', str(tempH))   
    dWCLog.insert('0.0', str(dTempWC))
    
    secLog.delete('0.0', 'end')
    minCLog.delete('0.0', 'end')
    maxCLog.delete('0.0', 'end')
    minWLog.delete('0.0', 'end')
    maxWLog.delete('0.0', 'end')
    minALog.delete('0.0', 'end')
    maxALog.delete('0.0', 'end')
    minWTCTLog.delete('0.0', 'end')
    maxWTCTLog.delete('0.0', 'end')
    
    secLog.insert('0.0', secList)
    minCLog.insert('0.0', str(minC))
    minWLog.insert('0.0', str(minW))
    minALog.insert('0.0', str(minA))
    minWTCTLog.insert('0.0', str(min(dTempWCL)))
    
    maxCLog.insert('0.0', str(maxC))
    maxWLog.insert('0.0', str(maxW))
    maxALog.insert('0.0', str(maxA))
    maxWTCTLog.insert('0.0', str(max(dTempWCL)))
    
    
    


# - CREATING THE CANVAS
canvas = FigureCanvasTkAgg(f, master=leftSide)
canvas.show()
canvas.get_tk_widget().grid(row=0, column=0, sticky='NESW')

'''
button1 = Button(bottomRight, text="RESET Test", command=resetButton).pack(side=BOTTOM)# - LATER PUT IN A NAV BAR FOR STYLING PURPOSES
'''
button2 = Button(bottomSide, text="SAVE Test", command=lambda: saveButton())
button2.grid(row=7, column=5, sticky='SE', padx=15, pady=15)

ani = animation.FuncAnimation(f, animate, interval=1000)
root.mainloop()
