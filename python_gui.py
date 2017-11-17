""" Author: Goran Popovic """
""" Python version: 3.5 """

""" GUI which consists of grid and control buttons sends selected values
    over serial port to Arduino Uno board (programmed with "arduno_code.ini").
    
    Arduino receives values and decodes them and writes values on digital pins accordingly.
    Digital pins are connected to the two R-2R ladder and each ladder is connected to one channel
    of the oscilloscope. The oscilloscope is in x-y mode and shows the pixels drawn in GUI""" 

from tkinter import *
import serial

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
        self.s=serial.Serial('/dev/ttyACM0',baudrate=115200)     
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
        
class App:
        def __init__(self, master):
            frame=Frame(master)
            frame.pack()
            grid=CellGrid(frame,64,64,10);
            grid.pack()
            self.button=Button(frame,text="Quit", fg="red", command=quit)
            self.button.pack(side=LEFT)
            self.button=Button(frame,text="Clear", fg="green", command=grid.clear)
            self.button.pack(side=LEFT)
            self.button=Button(frame,text="Print", fg="blue", command=grid.serialStart)
            self.button.pack(side=LEFT)
            self.button=Button(frame,text="Stop", fg="blue", command=grid.stop)
            self.button.pack(side=LEFT)


            
if __name__ == "__main__" :
    root = Tk()
    app=App(root)
    root.mainloop()   
