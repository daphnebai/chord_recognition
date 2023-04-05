import time
import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

#输入文件预处理
f=open('in2.txt','r',encoding='utf-8')
line=f.read();
line=line.split() #生成包含文本文件的列表
count=1
newLine=[] #记录项内容
newCount=[] #记录插入重复次数
length=len(line)
#合并连续的相同项，并标注重复次数
for i in range(0,length-1):
    if line[i]==line[i+1]:
        count=count+1 #重复次数加一
    else:
        newLine.append(line[i]) #插入项内容
        newCount.append(count) #插入重复次数
        count=1
#文件尾部处理
newLine.append(line[length-1])
newCount.append(count)
length=len(newLine)
#print(newLine)
#print(newCount)

#pygame库用于播放音频文件,pygame初始化
pygame.init()
pygame.mixer.init()
musicPlayingFlag=0       #音频是否在播放的标志，0表示停止，1表示播放

#GUI初始化
root = tk.Tk()
root.title("和弦识别系统")
root.geometry("600x340")
backgroundImage=PhotoImage(file=r"background.png") #添加背景图片
background_label=tk.Label(image=backgroundImage)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas=Canvas(root,bg="white",width=300,height=200) #建立一个画布对象canvas，属于tk对象
canvas.place(x=250,y=70,anchor=tk.NW) #将画布对象更新显示在框架中
canvas.create_text(150,100,text='',font=("Helvetica", 40)) #添加文字，属于canvas对象
canvas.create_text(250,100,text='',font=("Helvetica", 20)) #添加文字，属于canvas对象
canvas.create_rectangle(5, 5, 300, 200,
outline='black', # 边框颜色
width=2 # 边框宽度
)

#画布重画
def canvasRepaint():
    print("repaint")
    canvas.coords(1,150,100)
    canvas.coords(2,250,100)
    canvas.itemconfigure(1,text='',font=("Helvetica", 40))  #左边的字符串瞬移到最右端，并改变其内容和大小
    canvas.itemconfigure(2,text='',font=("Helvetica", 20)) 
    root.update()


#显示歌曲名  
var = ""
text = tk.StringVar()
       
lbl = tk.Label(
    root, 
    font=("Arial", 15),
    bg="white",
    textvariable=text
).place(x=250, y=20) 

#打开文件按钮
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

#播放按钮，开始播放音乐，同时调用Cartoon（），播放对应动画
def PLAY():
    if var != "":
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(var)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy()==0:
            time.sleep(0.01)
        global musicPlayingFlag
        musicPlayingFlag=1
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

#停止按钮
def Stop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    global musicPlayingFlag
    musicPlayingFlag=0
    
stopButton=PhotoImage(file=r"stop.png")
stop = tk.Button(
    root,
    height=40,
    width=40,
    image=stopButton,
    command=Stop
).place(x=170, y=20)

#音量调节
def setVolume(vol):
    pygame.mixer.music.set_volume(int(vol)/100)

tk.Label(
    root, 
    font=("Arial", 10),
    bg="white",
    text="音量(Volume)"
).place(x=30, y=70) 
slid_var = DoubleVar()
slid_var.set(100)
slider = Scale(
    root,
    from_=0, to=100, 
    orient=HORIZONTAL,
    command=setVolume,
    variable=slid_var,
    bg="white"
).place(x=30, y=90)

#功能选择（下拉框）
tk.Label(
    root, 
    font=("Arial", 10),
    bg="white",
    text="功能选择(Function)"
).place(x=30, y=140)

# 创建下拉菜单
cbox = ttk.Combobox(root)
# 使用 grid() 来控制控件的位置
cbox.place(x=30,y=160)
# 设置下拉菜单中的值
cbox['value'] = ('Original','Simplified')
#通过 current() 设置下拉菜单选项的默认值
cbox.current(0)

# 编写回调函数，绑定执行事件,向文本插入选中文本
def func(event):
    text.insert('insert',cbox.get()+"\n")
    if cbox.get()=='Original':
        state=0
    else:
        state=1
# 绑定下拉菜单事件
cbox.bind("<<ComboboxSelected>>",func)

#调性显示动画效果
def Cartoon():
    global musicPlayingFlag
    for i in range (0,length-1):
        if musicPlayingFlag==0: 
            canvasRepaint()
            return  
        for j in range(0,20):                 #建立一个60次的循环 ，循环区间[0,59）
            canvas.move(1,-5,0)               #默认图形编号为1，用于函数调用，以后的图形编号顺序类推。canvas对象中的编号“1”图形调用移动函数，x轴5个像素点，y轴不变
            canvas.move(2,-5,0)
            root.update()                           #更新框架，强制显示改变
            time.sleep(newCount[i]/200)           #睡眠newCount[i]/200秒，制造帧与帧间的间隔时间，保证采样率
        canvas.move(i%2+1,200,0)
        canvas.itemconfigure(i%2+1, text=newLine[i],font=("Helvetica", 20))  #左边的字符串瞬移到最右端，并改变其内容和大小
        canvas.itemconfigure((i+1)%2+1,font=("Helvetica", 40)) 
        root.update()
        time.sleep(0.05)

#显示窗口
root.mainloop()
