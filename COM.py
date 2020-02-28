import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
import time
import webbrowser
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolledtext
from tkinter import filedialog
import serialPort
import sys
import portList

serialport = serialPort.SerialPort()
logFile = None
ports_list = portList.serial_ports()

root = tk.Tk()
root.title("COM Port - Serial Data Terminal")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/3
window_height = screen_width/4
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d'%(window_width, window_height, window_position_x, window_position_y))

def cleardata():
    textbox.delete(1.0, END)

def exitapp():
    sys.exit(0)

def ReceiveData(message):
    str_message= message.decode('utf-8')
    str_message.config(font = ("bold", 5))
    textbox.insert('1.0', str_message)

serialport.RegisterReceiveCallBack(ReceiveData)

def loop_main():
    root.after(200, loop_main)

def OpenCommand():
    if close_com_button.cget("text") == "Open COM Port":
        comport=comport_combobox.get()
        baudrate= baud_rate_combobox.get()
        serialport.Open(comport, baudrate)
        close_com_button.config(text="Close COM Port")
        textbox.insert('1.0', "COM Port Opened\r\n")
    elif close_com_button.cget("text")=='Close COM Port':
        if replay_log_button.cget("text")  == "Stop Replay Log":
            textbox.insert('1.0', "Stop Log Replay first\r\n")
        else:
            serialport.Close()
            close_com_button.config(text='Open COM Port')
            textbox.insert('1.0', "COM Port Closed\r\n")

def SendData():
    message = mess_box.get()
    if serialport.IsOpen():
        message +='\r\n'
        serialport.Send(message)
        textbox.insert('1.0', message)
    else:
        textbox.insert ('1.0', "Not sent - COM Port is closed\r\n")

def ReplayLogThread():
    while True:
        time.sleep(1.0)
        global logFile
        if serialPort.IsOpen():
            if logFile != None:
                ReplayLogFile()

def ReplayLogFile():
    try:
        if logFile != None:
            readline = logFile.readline()
            global serialport
            serialport.Send(readline)
    except:
        print ("Exception in ReplayLogFile()")

def OpenLogFile():
    if not serialport.IsOpen():
        textbox.insert('1.0',"Open COM Port first\r\n")
    else:
        if replay_log_button.cget('text') == 'Replay Log':
            try:
                root.filename = filedialog.askopenfilename(initialdir="/", title = "Select file",filetypes=(("log files", "*.log"), ("all files", "*.*")))
                global logFile
                logFile = open(root.filename, 'r')
                _thread.start_new_thread(ReplayLogThread, ())
                replay_log_button.config(text="Stop Log Replay")
                textbox.insert('1.0', "Sending to open COM port from: "+root.filename+'\r\n') 
            except:
                textbox.insert('1.0', "Could not open file\r\n")
        else:
            replay_log_button.config(text = "Replay Log")
            textbox.insert('1.0', "Stopped sending message to open COM port\r\n")
            logFile = None

textbox = tkscrolledtext.ScrolledText(root, wrap = 'word', width = 28, height = 7)
textbox.pack(side = "left", expand = "no", padx=19, pady =10)
textbox.place(x=20, y=197)
textbox.config(font= ("bold"))

messenger_label = Label (root, height =2, width =10, text = "Messenger")
messenger_label.pack()
messenger_label.place(x= 10, y=120)
messenger_label.config(font = "bold")

mess_box = Entry(root, width =20)
mess_box.pack()
mess_box.place(x=110, y=133)

send_mess_button = Button(root, text = "Send Message", width = 15, height = 1, command = SendData)
send_mess_button.pack()
send_mess_button.place(x= 300, y=130)

replay_log_button = Button(root, text = "Replay Log", width = 15, height = 1, command = OpenLogFile)
replay_log_button.pack()
replay_log_button.place(x= 300, y=232)

clear_data_button = Button(root, text = "Clear Rx Data", width = 15, height = 1, command = cleardata)
clear_data_button.pack()
clear_data_button.place(x= 300, y=265)

exit_button = Button(root, text = "Exit", width = 15, height = 1, command = exitapp)
exit_button.pack()
exit_button.place(x= 300, y=300)

close_com_button = Button(root, text = "Open COM Port", width = 15, height = 1, command = OpenCommand)
close_com_button.pack()
close_com_button.place(x= 300, y=200)

connect_frame = LabelFrame(root, text = "Connect",width = 215, height = 100, font = ("bold", 10))
connect_frame.pack()
connect_frame.place(x= 20, y= 10)

comport_label = Label(connect_frame, height =2, width =10, text = "COM Port")
comport_label.pack()
comport_label.place(x= 5, y=0)


comport_combobox = Combobox(connect_frame, width =6)
comport_combobox['values']=(ports_list)
comport_combobox.current(0)
comport_combobox.pack()
comport_combobox.place(x=80, y=8)


baud_rate_label = Label(connect_frame, height= 2, width=10, text = "Baud Rate")
baud_rate_label.pack()
baud_rate_label.place(x=5, y=30)

baud_rate_combobox = Combobox(connect_frame, width= 6)
baud_rate_combobox['values']= (9600, 19200, 28800, 38400, 56600, 115200)
baud_rate_combobox.current(3)
baud_rate_combobox.place(x= 80, y=37)

root.after(200, loop_main)

root.mainloop()
