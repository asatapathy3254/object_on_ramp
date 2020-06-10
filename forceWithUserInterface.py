import tkinter as tk
from PIL import ImageTk,Image
global entry
global colour
import math
from math import ceil, floor


g = 9.8
Rdir = "FLAT"

root = tk.Tk()
canvas1 = tk.Canvas(root, width=800, height=550)
canvas1.pack()

labeltop = tk.Label(root, text='User Input')
labeltop.config(font=('Arial', 20))
canvas1.create_window(400, 40, window=labeltop)

width = 550
height = 300
path = 'images/ExampleOfForce.jpg'
img = Image.open(path)
img = img.resize((width, height), Image.ANTIALIAS)
photoImg = ImageTk.PhotoImage(img)
canvas1.create_image(390, 210, image=photoImg)

errorLab = tk.Label(root, text='Enter Numeric values only')
errorLab.config(font=('Arial', 9))
errorLab.config(bg="red")
canvas1.create_window(700, 375, window=errorLab)

RangLab = tk.Label(root, text='What is the angle between the ramp and horizontal (in degrees -90 <= Ө <= 90)?  ')
RangLab.config(font=('Arial', 9))
canvas1.create_window(400, 400, window=RangLab)
RangBox = tk.Entry(root)
canvas1.create_window(700, 400, window=RangBox)

mLab = tk.Label(root, text='Mass (kg): ')
mLab.config(font=('Arial', 9))
canvas1.create_window(590, 420, window=mLab)
mBox = tk.Entry(root)
canvas1.create_window(700, 420, window=mBox)

FappLab = tk.Label(root, text='Magnitude of Force Applied (N): ')
FappLab.config(font=('Arial', 9))
canvas1.create_window(533, 440, window=FappLab)
FappBox = tk.Entry(root)
canvas1.create_window(700, 440, window=FappBox)

FangLab = tk.Label(root, text='Angle of applied force (degrees): ')
FangLab.config(font=('Arial', 9))
canvas1.create_window(529, 460, window=FangLab)
FangBox = tk.Entry(root)
canvas1.create_window(700, 460, window=FangBox)

coefLab = tk.Label(root, text='Coefficient of friction (If no friction, input 0): ')
coefLab.config(font=('Arial', 9))
canvas1.create_window(505, 480, window=coefLab)
coefBox = tk.Entry(root)
canvas1.create_window(700, 480, window=coefBox)


def floatRound(num, places): #rounds a number to a given decimal place
    index = str(num).find('.')
    x = str(num)[int(index)+1:]
    if (len(x)>=places+1):
        y = x[places: places + 1]
        if (int(y)>=5):
            n = ceil(num * (10**places)) / float(10**places)
        else:
            n = floor(num * (10**places)) / float(10**places)
    else:
        n = num
    return n

#X component of gravity relative to the surface the object is on
def GforceX(m, a, Rdir):
    if (Rdir == "RIGHT" or Rdir == "LEFT"):
        F = (-1)*(m)*(g)*floatRound(math.sin(math.radians(a)), 2)
    else:
        F= 0
    return floatRound(F, 3)

#Y component of gravity relative to the surface the object is on
def GforceY(m, a):
    F = (-1)*(m)*(g)*floatRound(math.cos(math.radians(a)), 2)
    return floatRound(F, 3)

#X component of the applied force
def AppForceX(F, a):
    Fx = (F)*floatRound(math.cos(math.radians(a)),2)
    return floatRound(Fx, 3)

#Y component of the applied force
def AppForceY(F, a):
    Fy = (F)*floatRound(math.sin(math.radians(a)),2)
    return floatRound(Fy, 3)

#Normal force
def NormForce(Fg, Fy):
    if((Fg+Fy)< 0):
        Fn = (-1)*(Fg+Fy)
    elif((Fg+Fy)>0):
        Fn = 0
    else:
        Fn = (Fg + Fy)
    print (Fn)
    return floatRound(Fn, 3)

#returns the direction the object is moving in
def checkMotion(F1, F2, F3):
    F = F1 + F2 + F3
    if (F>0):
        d = 1 #motion is to the right
        n = "right"
    elif (F<0):
        d = -1 #motion is to the left
        n = "left"
    else:
        d = 0 #no motion
        n = ""
    return d, n.upper()

#friction force
def FricForce(c, Fn, dir, Fy, Fg):
    if (Fy + Fg > 0):
        Ff = 0
    else:
        if (dir == 1):
            Ff = (-1)*(c)*(Fn)
        elif (dir == -1):
            Ff = (c) * (Fn)
        else:
            Ff = 0
    return floatRound(Ff, 3)

#Y component of the Net force relative to the surface the object is on
def NetForceY(Fn, Fg, Fy):
    NFy = floatRound(Fn + Fg + Fy, 3)
    return NFy

#X component of Net force
def NetForceX(Fx, Ff, Fg):
    if (abs(Ff)> abs(Fx+Fg)):
        NFx = 0
    else:
        NFx = floatRound(Fx + Ff + Fg, 3)
    return NFx

#acceleration
def accel(F, m):
    if (m > 0):
        a = F/m
    else:
        a = 0
    return a

def Calculator(Rang, m , Fapp, Fang, coef):
    if (Rang > 0):
        Rdir = "RIGHT"
    elif (Rang < 0):
        Rdir = "LEFT"
    else:
        Rdir = "FLAT"

    Fgy = GforceY(m, Rang)
    print("Fgy = " + str(Fgy))
    Fgx = GforceX(m, Rang, Rdir)
    print("Fgx = " + str(Fgx))
    Fappx = AppForceX(Fapp, Fang)
    print("Fappx = " + str(Fappx))
    Fappy = AppForceY(Fapp, Fang)
    print("Fappy = " + str(Fappy))
    Fnorm = NormForce(Fgy, Fappy)
    print("Fnorm = " + str(Fnorm))
    dir, dirword = checkMotion(Fappx, Fgx, 0)
    Ffric = FricForce(coef, Fnorm, dir, Fappy, Fgy)
    print("Ffric = " + str(Ffric))
    NFx = NetForceX(Fappx, Ffric, Fgx)
    print("NFx = " + str(NFx))
    NFy = NetForceY(Fnorm, Fgy, Fappy)
    print("NFy = " + str(NFy))
    ax = accel(NFx, m)
    ay = accel(NFy, m)

    # Printing results
    if (ax != 0):
        if (Rdir != "FLAT"):
            if (dirword == Rdir):
                motion = "up"
            else:
                motion = "down"
            phrase = ("Accelerating " + motion + " the ramp at " + str(floatRound(ax, 2)) + " m/s^2")

        else:
            phrase = ("Accelerating to the " + dirword.lower() + " at " + str(floatRound(ax, 2)) + " m/s^2")
    else:
        phrase = ("Object is not accelerating.")
    print (phrase)
    return (Fgy, Fgx, Fappx, Fappy, Fnorm, Ffric, NFx, NFy, phrase)

def label(canvas, vari, size, x, y):
    vari.config(font=('Arial', size))
    canvas.create_window(x, y, window = vari)

def outputWin(Fgy, Fgx, Fappx, Fappy, Fnorm, Ffric, NFx, NFy, phrase):
    canvas1.destroy()
    canvas2 = tk.Canvas(root, width=800, height=550)
    canvas2.pack()
    LabelTop = tk.Label(root, text='Results')
    label(canvas2, LabelTop, 20, 400, 50)
    RangLab = tk.Label(root, text=("Ramp Angle: " + RangBox.get()))
    label(canvas2, RangLab, 9, 100, 100)
    mLab = tk.Label(root, text=("Mass: " + mBox.get()))
    label(canvas2, mLab, 9, 265, 100)
    FappLab = tk.Label(root, text=("Applied Force: " +FappBox.get()))
    label(canvas2, FappLab, 9, 400, 100)
    FangLab = tk.Label(root, text=("Angle of Force: " + FangBox.get()))
    label(canvas2, FangLab, 9, 535, 100)
    coefLab = tk.Label(root, text=("Coefficient of Friction: " + coefBox.get()))
    label(canvas2, coefLab, 9, 690, 100)
    FgxLab = tk.Label(root, text=("X-component of gravitational Force: " + str(Fgx)))
    label(canvas2, FgxLab, 15,400, 150)
    FgyLab = tk.Label(root, text=("Y-component of gravitational Force: " + str(Fgy)))
    label(canvas2, FgyLab, 15, 400, 180)
    FappxLab = tk.Label(root, text=("X-component of applied Force: " + str(Fappx)))
    label(canvas2, FappxLab, 15,400, 210)
    FappyLab = tk.Label(root, text=("Y-component of applied Force: " + str(Fappy)))
    label(canvas2, FappyLab, 15, 400, 240)
    FnormLab = tk.Label(root, text=("Normal Force: " + str(Fnorm)))
    label(canvas2, FnormLab, 15, 400, 270)
    FfricLab = tk.Label(root, text=("Friction Force: " + str(abs(Ffric))))
    label(canvas2, FfricLab, 15, 400, 300)
    NFxLab = tk.Label(root, text=("X-component of Net Force: " + str(NFx)))
    label(canvas2, NFxLab, 15, 400, 330)
    NFyLab = tk.Label(root, text=("Y-component of Net Force: " + str(NFy)))
    label(canvas2, NFyLab, 15, 400, 360)
    phraseLab = tk.Label(root, text=(str(phrase)))
    label(canvas2, phraseLab, 20, 400, 400)



def values():
    Rang = float(RangBox.get())
    m = float(mBox.get())
    Fapp = float(FappBox.get())
    Fang = float(FangBox.get())
    coef = float(coefBox.get())
    print(Rang, m, Fapp, Fang, coef)
    Fgy, Fgx, Fappx, Fappy, Fnorm, Ffric, NFx, NFy, phrase = Calculator(Rang, m, Fapp, Fang, coef)
    outputWin(Fgy, Fgx, Fappx, Fappy, Fnorm, Ffric, NFx, NFy, phrase)


button1 = tk.Button(root, text=' Next ', command=values, bg='gray', font=('Arial', 11, 'bold'))
canvas1.create_window(700, 520, window=button1)
root.mainloop()








# entry3 = tk.Entry(root)
# canvas1.create_window(400, 140, window=entry3)
#
#
# def create_charts():
#     global x1
#     global x2
#     global x3
#     global bar1
#     global pie2
#     x1 = float(entry1.get())
#     x2 = float(entry2.get())
#     x3 = float(entry3.get())
#
#     figure1 = Figure(figsize=(4, 3), dpi=100)
#     subplot1 = figure1.add_subplot(111)
#     xAxis = [float(x1), float(x2), float(x3)]
#     yAxis = [float(x1), float(x2), float(x3)]
#     subplot1.bar(xAxis, yAxis, color='lightsteelblue')
#     bar1 = FigureCanvasTkAgg(figure1, root)
#     bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
#
#     figure2 = Figure(figsize=(4, 3), dpi=100)
#     subplot2 = figure2.add_subplot(111)
#     labels2 = 'Label1', 'Label2', 'Label3'
#     pieSizes = [float(x1), float(x2), float(x3)]
#     my_colors2 = ['lightblue', 'lightsteelblue', 'silver']
#     explode2 = (0, 0.1, 0)
#     subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True,
#                  startangle=90)
#     subplot2.axis('equal')
#     pie2 = FigureCanvasTkAgg(figure2, root)
#     pie2.get_tk_widget().pack()
#
#
# def clear_charts():
#     bar1.get_tk_widget().pack_forget()
#     pie2.get_tk_widget().pack_forget()
#
#
# button1 = tk.Button(root, text=' Create Charts ', command=create_charts, bg='palegreen2', font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 180, window=button1)
#
# button2 = tk.Button(root, text='  Clear Charts  ', command=clear_charts, bg='lightskyblue2', font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 220, window=button2)
#
# button3 = tk.Button(root, text='Exit Application', command=root.destroy, bg='lightsteelblue2',
#                     font=('Arial', 11, 'bold'))
# canvas1.create_window(400, 260, window=button3)
#

# def check():
#     try:
#         Rang = float(RangBox.get())
#         m = float(mBox.get())
#         Fapp = float(FappBox.get())
#         Fang = float(FangBox.get())
#         coef = float(coefBox.get())
#         print(Rang, m, Fapp, Fang, coef)
#         errorLab.destroy()
#     except:
#         errorLab = tk.Label(root, text='Enter Numeric values only')
#         errorLab.config(font=('Arial', 9))
#         errorLab.config(bg="red")
#         canvas1.create_window(700, 380, window=errorLab)
#         x=1
#         return
    # y = 1
    # while (y == 1):
    #     RangBnds = 1
    #     mBnds = 1
    #     FappBnds = 1
    #     FangBnds = 1
    #     coefBnds = 1
    #     if (Rang < -90 or Rang > 90):
    #         RangBnds = 2
    #     if (m < 0):
    #         mBnds = 2
    #     if (Fapp < 0):
    #         FappBnds = 2
    #     if (Fang > 360):
    #         FangBnds = 2
    #     if (coef < 0):
    #         coefBnds = 2
    #     if (RangBnds == 1 and mBnds == 1 and FappBnds == 1 and FangBnds == 1 and coefBnds == 1):
    #         print ("ok")
    #         y = 2
    #     else:
    #         if (RangBnds == 2):
    #             RangBox.configure({"background": "red"})
    #         if (mBnds == 2):
    #             mBox.configure({"background": "red"})
    #         if (FappBnds == 2):
    #             FappBox.configure({"background": "red"})
    #         if (FangBnds == 2):
    #             FangBox.configure({"background": "red"})
    #         if (coefBnds == 2):
    #             coefBox.configure({"background": "red"})
    # return


# def next():
#     RangBnds = 1
#     mBnds = 1
#     FappBnds = 1
#     FangBnds = 1
#     coefBnds = 1
#     RangBnds, mBnds, FappBnds, FangBnds, coefBnds = check()
#
