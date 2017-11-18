""" Author: Goran Popovic """
""" Python version: 3.5 """

""" GUI which consists of grid and control buttons sends selected values
    over serial port to Arduino Uno board (programmed with "arduno_code.ini").
    
    Arduino receives values and decodes them and writes values on digital pins accordingly.
    Digital pins are connected to the two R-2R ladder and each ladder is connected to one channel
    of the oscilloscope. The oscilloscope is in x-y mode and shows the pixels drawn in GUI""" 
    
    
    
icm_dots=(( 3, 7),( 3, 5),( 2, 5),( 2, 7),( 2, 9),( 2,11),( 2,13),
          ( 3,13),( 3,11),( 3, 9),( 3, 7),( 5, 7),( 5, 9),( 5,11),
          ( 6,12),( 7,13),( 8,13),( 9,13),(10,13),(11,12),(11,11),
          (10,11),( 9,12),(7.5,12),( 6,11),( 6, 9),( 6, 7),(7.5,6),
          ( 9, 6),(10, 7),(11, 7),(11, 6),(10, 5),( 9, 5),( 8, 5),
          ( 7, 5),( 6, 6),( 5, 7),(13, 5),(13, 7),(13, 9),(13,11),
          (13,13),(14,13),(15,12),(16,11),(17,12),(18,13),(19,13),
          (19,11),(19, 9),(19, 7),(19, 5),(18, 5),(18, 7),(18, 9),
          (18,11),(17,10),(16, 9),(15,10),(14,11),(14, 9),(14, 7),
          (14, 5),(13, 5))    
    

from tkinter import *
import sys
import glob
import serial
import time


""" source: https://github.com/LVH-27/S3-ROV/blob/master/2017/komp/ipak_python/ROVserial.py"""
def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    if len(result) == 0:
        print("No serial connection available!")
        quit(-1)
    elif len(result) > 1:
        while True:
            print("Several serial connections available!\nChoose one by writing the list index:")
            try:
                for i in range(len(result)):
                    print(i, result[i])
                port_index = int(input())
                COMM_PORT = result[port_index]
                break
            except IndexError as ie:
                print("Index out of range!\n")
            except ValueError as ve:
                print("Invalid input value!\n")

    else:
        COMM_PORT = result[0]
    return COMM_PORT


class Cell():
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False

    def _set(self):
        """ Set the cell """
        self.fill= True;

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.FILLED_COLOR_BG="#96fffd"
            outline = Cell.FILLED_COLOR_BORDER= "#96fffd"

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG="#247e87"
                outline = Cell.EMPTY_COLOR_BORDER= "#187c7a"

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been set
        self.set = []
        self.coordinates=[]

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.set.clear())
        
        self.draw()
        self.pool=True
        self.s=serial.Serial(serial_ports(),baudrate=115200)     
        self.counter=0

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._set()
        cell.draw()
        #add the cell to the list of cell set during the click
        self.set.append(cell)
        self.coordinates.append((column,63-row))


    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        if cell not in self.set:
            cell._set()
            cell.draw()
            self.set.append(cell)
            self.coordinates.append((column,63-row))
            
    def clear(self):
        self.set=[]
        self.coordinates=[]
        for row in self.grid:
            for cell in row:
                cell.fill=False
                cell.draw()
           
    
                
        
    def serialStart(self):
        self.pool=True
        self.serialLoop()
        
    def serialLoop(self):
        if self.pool:            
            self.counter=self.counter+1
            self.counter=self.counter%len(self.coordinates)
            i=self.coordinates[self.counter]     
            string="S"+chr(4*i[0])+chr(4*i[1])+"\r\n"
            self.s.write(bytes(string,"iso-8859-1"))
            self.after(0,self.serialLoop)

    def stop(self):
        self.pool=False    
        
    def draw_ICM(self):
        self.clear()
        x=3.3
        resized_icm_dots=[]
        for i in icm_dots:
            resized_icm_dots.append((int(i[0]*x),int(i[1]*x)))
        for i in resized_icm_dots:
            cell = self.grid[64-i[1]][i[0]]
            cell._set()
            self.set.append((64-i[1],i[0]))
            self.coordinates.append(i)
        self.draw()
class App:
        def __init__(self, master):
            frame=Frame(master)
            frame.pack()
            grid=CellGrid(frame,64,64,10);
            grid.pack()
            self.button1=Button(frame,text="Quit", fg="red", command=quit)
            self.button1.pack(side=LEFT)
            self.button2=Button(frame,text="Clear", fg="green", command=grid.clear)
            self.button2.pack(side=LEFT)
            self.button3=Button(frame,text="Print", fg="blue", command=grid.serialStart)
            self.button3.pack(side=LEFT)
            self.button4=Button(frame,text="Stop", fg="blue", command=grid.stop)
            self.button4.pack(side=LEFT)
            self.button5=Button(frame,text="ICM",font=(14), fg="cyan", command=grid.draw_ICM)
            self.button5.pack(side=LEFT)
            
if __name__ == "__main__" :
    root = Tk()
    app=App(root)
    root.mainloop()   
