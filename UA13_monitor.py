import re
from tkinter import *
from tkinter import filedialog
from numpy import append, insert, record
import serial
import time
import openpyxl
from datetime import datetime


monitor = Tk()
monitor.title('Temp_monitor')
monitor.geometry("740x320")
monitor.resizable(False, False)

text_font = ("Boulder", 50, 'bold')
background = "#f2e750"
foreground = "#363529"

label1 = Label(monitor, width=5, font=text_font)
label2 = Label(monitor, width=5, font=text_font)
label3 = Label(monitor, width=5, font=text_font)
label4 = Label(monitor, text='T1 =', font=text_font)
label5 = Label(monitor, text='T2 =', font=text_font)
label6 = Label(monitor, text='T3 =', font=text_font)
label7 = Label(monitor, width=10, text='VALVE', font=text_font)
label8 = Label(monitor, width=10, font=text_font, fg='#ff1500')

label1.place(x=160, y=0)
label2.place(x=160, y=100)
label3.place(x=160, y=200)
label4.place(x=0, y=0)
label5.place(x=0, y=100)
label6.place(x=0, y=200)
label7.place(x=400, y=0)
label8.place(x=400, y=100)

def temp1_set():
    ser1 = serial.Serial("COM12", 19200, timeout=1)
    ser1.write(b'ATCD\r\n')
    global temp1
    temp1 = float((ser1.readline()[4:9]).split()[0])
    ser1.close()
    label1.config(text=str(temp1) + '℃')

def temp2_set():
    ser2 = serial.Serial("COM13", 19200, timeout=1)
    ser2.write(b'ATCD\r\n')
    global temp2
    temp2 = float((ser2.readline()[4:9]).split()[0])
    ser2.close()
    label2.config(text=str(temp2) + '℃')

def temp3_set():
    ser3 = serial.Serial("COM14", 19200, timeout=1)
    ser3.write(b'ATCD\r\n')
    global temp3
    temp3 = float((ser3.readline()[4:9]).split()[0])
    ser3.close()
    label3.config(text=str(temp3) + '℃')

def temp_monitor():
    temp1_set()
    temp2_set()
    temp3_set()
    monitor.after(1000, temp_monitor)

valve_value = False
record_value = False

set_temp = Entry(monitor, width=10)
set_temp.place(x=490, y=230)

def on():
    global valve_value
    global set_t
    set_t = float(set_temp.get())
    valve_value = True
    return valve_value

def off():
    global valve_value
    valve_value = False
    return valve_value

def valve_button():
    global valve_value
    ser4 = serial.Serial('COM11', 9600)
    if valve_value == True:
        if temp2 > float(set_t): #t1 상관없이
            valve_sig = '0'
            valve_signal = valve_sig.encode('utf-8')
            ser4.write(valve_signal) #밸브 열림
            label8.config(text='open')
        elif temp1 < float(set_t) and temp2 < float(set_t): #t1 t2 둘 다 내려가야함 / t2 높으면 open 유지
            valve_sig = '1'
            valve_signal = valve_sig.encode('utf-8')
            ser4.write(valve_signal) #밸브 닫힘
            label8.config(text='close')
    else:
        valve_sig = '1'
        valve_signal = valve_sig.encode('utf-8')
        ser4.write(valve_signal) #밸브 닫힘
        label8.config(text='close')
    monitor.after(1000, valve_button)

valve_on = Button(monitor, text='Valve OPEN', command= on)
valve_on.place(x=570, y=226)

valve_off = Button(monitor, text='Valeve CLOSE', command= off)
valve_off.place(x=647, y=226)

def record_start():
    global record_value
    record_value = True
    return record_value

def record_end():
    global record_value
    record_value = False
    return record_value

record_on = Button(monitor, text='Recording START', command= record_start)
record_on.place(x=530, y=285)

record_off = Button(monitor, text='Recording STOP', command= record_end)
record_off.place(x=635, y=285)

def record_dir():
    monitor.dirName=filedialog.askdirectory(initialdir="./", title="Save Record file")
    txt.delete(0, "end")
    txt.insert(0, monitor.dirName)

txt = Entry(monitor, width=50)
txt.place(x=70, y=288)

btn = Button(monitor, text="save_directory",command=record_dir)
btn.place(x=430, y=285)

wb = openpyxl.Workbook()
sheet1 = wb['Sheet']
sheet1['A1'] = 'Time'
sheet1['B1'] = 'Temp1'
sheet1['C1'] = 'Temp2'
sheet1['D1'] = 'Temp3'
sheet1['E1'] = 'Valve_state'

def record_button():
    global record_value
    global txt
    global label8
    date = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    if record_value == True:
        sheet1.append([date, temp1, temp2, temp3, label8.cget("text")])
        wb.save(txt.get() + '/Record_Temp.xlsx')
    else:
        pass
    monitor.after(10000, record_button)

temp_monitor()
valve_button()
record_button()
monitor.mainloop()