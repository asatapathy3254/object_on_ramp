import math
from math import ceil, floor
from PIL import Image

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

g = 9.8
Rang = 100
Rdir = "FLAT"
Fang = -91

img = Image.open("ExampleOfForce.jpg")
img.show()

while (Rang<-90 or Rang>90):
    Rang = float(input("What is the angle between the ramp and horizontal (in degrees -90 <= Ө <= 90)?  "))
if (Rang>0):
    Rdir = "RIGHT"
elif (Rang<0):
    Rdir = "LEFT"
else:
    Rdir = "FLAT"


m = float(input("Mass (kg): "))

Fapp = float(input("Magnitude of Force Applied (N): "))
if (Fapp!=0):
    Fang = float(input("Angle of applied force (degrees): "))
coef = float(input("Coefficient of friction (If no friction, input 0): "))

#X component of gravity relative to the surface the object is on
def GforceX(m, a):
    if (Rdir == "RIGHT" or Rdir == "LEFT"):
        F = (-1)*(m)*(g)*floatRound(math.sin(math.radians(a)), 2)
    else:
        F= 0
    return floatRound(F, 3)

#Y component of gravity relative to the surface the object is on
def GforceY(m, a):
    F = (-1)*(m)*(g)*floatRound(math.cos(math.radians(a)),2)
    return floatRound(F, 3)

#X component of the applied force
def AppForceX(F, a):
    Fx = (F)*(math.cos(math.radians(a)))
    return floatRound(Fx, 2)

#Y component of the applied force
def AppForceY(F, a):
    Fy = (F)*(math.sin(math.radians(a)))
    return floatRound(Fy, 3)

#Normal force
def NormForce(Fg, Fy):
    if((Fg+Fy)< 0):
        Fn = (-1)*(Fg+Fy)
    elif((Fg+Fy)>0):
        Fn = 0
    else:
        Fn = (Fg + Fy)
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


Fgy = GforceY(m,Rang)
print ("Fgy = " + str(Fgy))
Fgx = GforceX(m, Rang)
print ("Fgx = " + str(Fgx))
Fappx = AppForceX(Fapp, Fang)
print ("Fappx = " + str(Fappx))
Fappy = AppForceY(Fapp, Fang)
print ("Fappy = " + str(Fappy))
Fnorm = NormForce(Fgy, Fappy)
print ("Fnorm = " + str(Fnorm))
dir, dirword = checkMotion(Fappx, Fgx, 0)
Ffric = FricForce(coef, Fnorm, dir, Fappy, Fgy)
print ("Ffric = " + str(Ffric))
NFx = NetForceX(Fappx, Ffric, Fgx)
print ("NFx = " + str(NFx))
NFy = NetForceY(Fnorm, Fgy, Fappy)
print ("NFy = " + str(NFy))
ax = accel(NFx, m)
ay = accel(NFy, m)

#Printing results
if (ax != 0):
    if (Rdir != "FLAT"):
        if (dirword == Rdir):
            motion = "up"
        else:
            motion = "down"
        print ("Accelerating " + motion + " the ramp at " + str(floatRound(ax, 2)) + " m/s^2")
    else:
        print ("Accelerating to the " + dirword.lower() + " at " +  str(floatRound(ax, 2)) + " m/s^2")
else:
    print("Object is not accelerating.")
