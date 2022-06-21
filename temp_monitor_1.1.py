import re
from tkinter import *
from tkinter import filedialog
from numpy import append, array
import serial
import time
import openpyxl
from datetime import datetime
from HIDRelay import hid_relay

temp_group1 = list(range(0,5))
temp_group2 = list(range(0,5))

monitor = Tk()
monitor.title('Temp_monitor')
monitor.geometry("740x320")
monitor.resizable(False, False)

text_font = ("Boulder", 50, 'bold')
text_font1 = ("Boulder", 35, 'bold')
background = "#f2e750"
foreground = "#363529"

label1 = Label(monitor, width=10, font=text_font)
label2 = Label(monitor, width=10, font=text_font)
label3 = Label(monitor, width=10, font=text_font)
label4 = Label(monitor, text='T1 =', font=text_font1)
label5 = Label(monitor, text='T2 =', font=text_font1)
label6 = Label(monitor, text='T3 =', font=text_font1)
label7 = Label(monitor, width=6, text='VALVE', font=text_font)
label8 = Label(monitor, width=6, font=text_font, fg='#ff1500')
sensor_1 = Entry(monitor, width=3)
sensor_2 = Entry(monitor, width=3)
sensor_3 = Entry(monitor, width=3)

label1.place(x=100, y=0)
label2.place(x=100, y=100)
label3.place(x=100, y=200)
label4.place(x=25, y=0)
label5.place(x=25, y=100)
label6.place(x=25, y=200)
label7.place(x=475, y=0)
label8.place(x=475, y=100)
sensor_1.place(x=30, y=60)
sensor_2.place(x=30, y=160)
sensor_3.place(x=30, y=260)

checkVar1 = IntVar()
checkVar2 = IntVar()
checkVar3 = IntVar()

check_1 = Checkbutton(monitor, text="Use", variable=checkVar1)
check_2 = Checkbutton(monitor, text="Use", variable=checkVar2)
check_3 = Checkbutton(monitor, text="Use", variable=checkVar3)

check_1.place(x=60, y=58)
check_2.place(x=60, y=158)
check_3.place(x=60, y=258)

def temp1_set():
    try:
        if checkVar1.get() == 1:
            ser1 = serial.Serial("COM"+sensor_1.get(), 19200, timeout=1)
            ser1.write(b'ATCD\r\n')
            global temp1
            temp1 = (((ser1.readline()[4:12]).split()[0]).decode('utf-8')).split(',')[0]
            ser1.close()
            label1.config(text=temp1 + '℃')
        else:
            temp1 = 0.0
            label1.config(text='--.-℃')
    except :
        temp1 = 0.0
        label1.config(text='No data')

def temp2_set():
    try:
        if checkVar2.get() == 1:
            ser2 = serial.Serial("COM"+sensor_2.get(), 19200, timeout=1)
            ser2.write(b'ATCD\r\n')
            global temp2
            temp2 = (((ser2.readline()[4:12]).split()[0]).decode('utf-8')).split(',')[0]
            ser2.close()
            label2.config(text=temp2 + '℃')
        else:
            temp2 = 0.0
            label2.config(text='--.-℃')
    except :
        temp2 = 0.0
        label2.config(text='No data')

def temp3_set():
    try:
        if checkVar3.get() == 1:
            ser3 = serial.Serial("COM"+sensor_3.get(), 19200, timeout=1)
            ser3.write(b'ATCD\r\n')
            global temp3
            temp3 = (((ser3.readline()[4:12]).split()[0]).decode('utf-8')).split(',')[0]
            ser3.close()
            label3.config(text=temp3 + '℃')
        else:
            temp3 = 0.0
            label3.config(text='--.-℃')
    except :
        temp3 = 0.0
        label3.config(text='No data')

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
    try:
        global valve_value
        global set_t
        set_t = float(set_temp.get())
        valve_value = True
        return valve_value
    except:
        pass

def off():
    global valve_value
    valve_value = False
    return valve_value

def valve_button():
    try:
        rc = hid_relay.RelayController()
        rc.open_device()
        rc.off_all()

        global valve_value
        temp_group1.append(temp1)
        temp_group1.pop(0)
        temp_group2.append(temp2)
        temp_group2.pop(0)
        if valve_value == True:
            if all(float(set_t) < i for i in temp_group2):
                valve_sig = '0'
                valve_signal = valve_sig.encode('utf-8')
                rc.on_relay(1)
                label8.config(text='Open')
                print("O1")
            elif all(float(set_t) < i for i in temp_group1) and all(float(set_t) > i for i in temp_group2):
                valve_sig = '1'
                valve_signal = valve_sig.encode('utf-8')
                rc.on_relay(1)
                label8.config(text='Open')
                print("O2")
            elif all(float(set_t) > i for i in temp_group1) and all(float(set_t) > i for i in temp_group2):
                valve_sig = '1'
                valve_signal = valve_sig.encode('utf-8')
                rc.off_relay(1)
                label8.config(text='Close')
                print("C1")
            # else:
            #     valve_sig = '1'
            #     valve_signal = valve_sig.encode('utf-8')
            #     rc.off_relay(1)
            #     label8.config(text='Close')
            #     print("C2")
        else:
            valve_sig = '1'
            valve_signal = valve_sig.encode('utf-8')
            rc.off_relay(1)
            label8.config(text='Close')
    except:
        label8.config(text='None')

    monitor.after(1000, valve_button)


valve_on = Button(monitor, text='Valve OPEN', command= on)
valve_on.place(x=570, y=226)

valve_off = Button(monitor, text='Valve CLOSE', command= off)
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
