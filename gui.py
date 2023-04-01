import time
import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

#�����ļ�Ԥ����
f=open('in2.txt','r',encoding='utf-8')
line=f.read();
line=line.split() #���ɰ����ı��ļ����б�
count=1
newLine=[] #��¼������
newCount=[] #��¼�����ظ�����
length=len(line)
#�ϲ���������ͬ�����ע�ظ�����
for i in range(0,length-1):
    if line[i]==line[i+1]:
        count=count+1 #�ظ�������һ
    else:
        newLine.append(line[i]) #����������
        newCount.append(count) #�����ظ�����
        count=1
#�ļ�β������
newLine.append(line[length-1])
newCount.append(count)
length=len(newLine)
#print(newLine)
#print(newCount)

#pygame�����ڲ�����Ƶ�ļ�,pygame��ʼ��
pygame.init()
pygame.mixer.init()

#GUI��ʼ��
root = tk.Tk()
root.title("����ʶ��ϵͳ")
root.geometry("600x340")
backgroundImage=PhotoImage(file=r"background.png") #��ӱ���ͼƬ
background_label=tk.Label(image=backgroundImage)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas=Canvas(root,width=300,height=200) #����һ����������canvas������tk����
canvas.place(x=250,y=70,anchor=tk.NW) #���������������ʾ�ڿ����
canvas.create_text(150,100,text='',font=("Helvetica", 40)) #������֣�����canvas����
canvas.create_text(250,100,text='',font=("Helvetica", 20)) #������֣�����canvas����
canvas.create_rectangle(5, 5, 300, 200,
outline='black', # �߿���ɫ
width=2 # �߿���
)

#��ʾ������  
var = ""
text = tk.StringVar()
       
lbl = tk.Label(
    root, 
    font=("Arial", 15),
    textvariable=text
).place(x=250, y=20) 

#���ļ���ť
def OpenFile():
    global var
    
    filetypes = (
        ('mp3 (*.mp3)', '*.mp3'),
        ('wav (*.wav)', '*.wav'),
        ('ogg (*.ogg)', '*.ogg'),
        ('wma (*.wma)', '*wma'),
        ('m4a (*.m4a)', '*.m4a'),
        ('flac (*.flac)', '*.flac'),
        ('aac (*.aac)', '*.aac'),
        ('All Files (*.*)', '*.*')
    )
    
    var = fd.askopenfilename(
        title = "open a file",
        initialdir = "/",
        filetypes=filetypes
    )
    
    y = var.split("/")[-1]
    z = y.split(".")[0]
    text.set(z)

openButton=PhotoImage(file=r"open.png")
Open = tk.Button(
    root,
    height=40,
    width=40,
    image=openButton,
    command=OpenFile
).place(x=30, y=20)

#���Ű�ť����ʼ�������֣�ͬʱ����Cartoon���������Ŷ�Ӧ����
def PLAY():
    if var != "":
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(var)
        pygame.mixer.music.play()
        Cartoon()
    else:
        showinfo(
            title="Invalid!",
            message="No file selected or invalid format!"
        )

startButton=PhotoImage(file=r"start.png")
play = tk.Button(
    root,
    height=40,
    width=40,
    image=startButton,
    command=PLAY
).place(x=100, y=20)

#ֹͣ��ť
def Stop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    
stopButton=PhotoImage(file=r"stop.png")
stop = tk.Button(
    root,
    height=40,
    width=40,
    image=stopButton,
    command=Stop
).place(x=170, y=20)

#��������
def setVolume(vol):
    pygame.mixer.music.set_volume(int(vol)/100)

tk.Label(
    root, 
    font=("Arial", 10),
    text="����(Volume)"
).place(x=30, y=70) 
slid_var = DoubleVar()
slid_var.set(100)
slider = Scale(
    root,
    from_=0, to=100, 
    orient=HORIZONTAL,
    command=setVolume,
    variable=slid_var
).place(x=30, y=90)

#����ѡ��������
tk.Label(
    root, 
    font=("Arial", 10),
    text="����ѡ��(Function)"
).place(x=30, y=140)

# ���������˵�
cbox = ttk.Combobox(root)
# ʹ�� grid() �����ƿؼ���λ��
cbox.place(x=30,y=160)
# ���������˵��е�ֵ
cbox['value'] = ('Original','Simplified')
#ͨ�� current() ���������˵�ѡ���Ĭ��ֵ
cbox.current(0)

# ��д�ص���������ִ���¼�,���ı�����ѡ���ı�
def func(event):
    text.insert('insert',cbox.get()+"\n")
    if cbox.get()=='Original':
        state=0
    else:
        state=1
# �������˵��¼�
cbox.bind("<<ComboboxSelected>>",func)

#������ʾ����Ч��
def Cartoon():
    for i in range (0,length-1):
        for j in range(0,20):                 #����һ��60�ε�ѭ�� ��ѭ������[0,59��
            canvas.move(1,-5,0)               #Ĭ��ͼ�α��Ϊ1�����ں������ã��Ժ��ͼ�α��˳�����ơ�canvas�����еı�š�1��ͼ�ε����ƶ�������x��5�����ص㣬y�᲻��
            canvas.move(2,-5,0)
            root.update()                           #���¿�ܣ�ǿ����ʾ�ı�
            time.sleep(newCount[i]/200)           #˯��newCount[i]/200�룬����֡��֡��ļ��ʱ�䣬��֤������
        canvas.move(i%2+1,200,0)
        canvas.itemconfigure(i%2+1, text=newLine[i],font=("Helvetica", 20))  #��ߵ��ַ���˲�Ƶ����Ҷˣ����ı������ݺʹ�С
        canvas.itemconfigure((i+1)%2+1,font=("Helvetica", 40)) 
        root.update()
        time.sleep(0.05)

#��ʾ����
root.mainloop()