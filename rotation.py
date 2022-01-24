# Equipo Spyders
    # Isabel Lucia Constantino Preciado
    # Arturo Jauregui Diaz
    # Jose Abraham Morales
    # Ivana Estefania Betancourt Navarro
    # Jorge Antonio Ruiz Zavalza
    # Creado el 26/02/19
    
from pylab import pi
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math
x = []
y = []
t = []
Ang = []
v = []
a = [] 
ymin =10000
ymax = 0
i=0
    
    #Starting camera
cap = cv2.VideoCapture('vid1.mov')
    
while(1):
        
    #Captura image and covert it RGB -> HSV
    ret, imagen = cap.read()
    if ret:
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
            
        # Establish the range of colors to detect
        color_bajos = np.array([0, 0, 0], np.uint8)
        color_altos = np.array([250, 250, 250], np.uint8)
        #Create a mask with only the white pixels inside the black square
        mask = cv2.inRange(hsv, color_bajos, color_altos)
        cnt = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
        #Show the original image with the mask with only white pixels
        cv2.imshow('hsv', mask)
    
        cnt = cnt[0]
        center = None
        if len(cnt) > 0:
            M = cv2.moments(cnt)
            #Look for the center of the object
            x.append(int(M["m10"] / M["m00"]))
            y.append(int(M["m01"] / M["m00"]))
            t.append(i/30)
            # Display rectangular coordinates
            print(x[i], y[i])
            if y[i] < ymin:
                ymin = y[i]
            if y[i] > ymax:
                ymax = y[i]
        
            i=i+1
    else:        
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
    
radio= (ymax-ymin)/2
Ang = []
Angcor = []
ang2 = 0
Angcor.append(0)
Ang.append(0)

# Calculate angular position
for i in range(1,len(x)):
    L=(((x[i]-x[i-1])**2)+((y[i]-y[i-1])**2))
    ang = math.acos(1-(L)/(2*radio**2))
    ang2 = ang2 + ang
    if ang2 >= 2*pi:
        ang2 = ang2 - 2*pi
    Angcor.append(ang2)
    Ang.append(Ang[i-1]+ang)

# Calculate angular velocity
v = []
v.append(0)
for i in range(1,len(t)):
    y1 = (Ang[i]-Ang[i-1])/(t[i]-t[i-1])
    v.append(y)

# Calculate angular acceleration
a=[]
a.append(0)
for i in range(1,len(t)):
    ac = (v[i]-v[i-1])/(t[i]-t[i-1])
    a.append(ac)

# Plotting
plt.plot(x, y, ',')
plt.title("Pos X vs Pos Y", fontsize=12)
plt.xlabel("Pos X", fontsize=10, color='green')
plt.ylabel("Pos Y", fontsize=10, color='green')
plt.savefig('Graph1.pdf')
plt.ylim(620,660)
plt.xlim(345,375)
plt.show()    

plt.plot(t, Ang, ',')
plt.title("Angular position vs Time", fontsize=12)
plt.xlabel("Time (s)", fontsize=10, color='green')
plt.ylabel("Angular position (rad)", fontsize=10, color='green')
plt.savefig('Graph2.pdf')
plt.show() 

plt.plot(t, Angcor, ',')
plt.title("Angular position vs Time (per period).", fontsize=12)
plt.xlabel("Time (s)", fontsize=10, color='green')
plt.ylabel("Position (rad)", fontsize=10, color='green')
plt.savefig('Graph3.pdf')
plt.show()

plt.plot(t, v, ',')
plt.title("Angular velocity vs Time", fontsize=12)
plt.xlabel("Time (s)", fontsize=10, color='green')
plt.ylabel("Velocity (rad/s)", fontsize=10, color='green')
plt.savefig('Graph4.pdf')
plt.ylim(-50,50)
plt.show()
    
plt.plot(t, a, ',')
plt.title("Angular acceleration vs Time", fontsize=12)
plt.xlabel("Time (s)", fontsize=10, color='green')
plt.ylabel("Acceleration (rad/s^2)", fontsize=10, color='green')
plt.savefig('Graph5.pdf')
plt.ylim(-700,700)
plt.show()