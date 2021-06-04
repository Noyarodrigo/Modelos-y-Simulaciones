#altura 0m gravedad 9.8m/s**2
#Primeros 2 dec del doc velocidad, 2 sig angulo
#reemplazar 0 con 1's
#Determinar alcance y altura max
import math
import numpy as np
import matplotlib.pylab as plt

doc = str(input('Ingrese su doc:')).replace("0","1",4)
vel,ang = int(doc[:2]), int(doc[2:4])
print('vel:{}, ang:{}'.format(vel,ang))

#Xmax = vo**2 . sen(2 ang)/g
#Ymax = vo**2 . sen**2(ang)/2g

xmax = ((vel**2)/9.8) * math.sin(math.radians(2*ang))
ymax = ((vel**2) * math.pow(math.sin(math.radians(ang)),2))/(2*9.8)

print(f"Xmax: {xmax:.2f}m\nYmax: {ymax:.2f}m")

t = np.linspace(0, 5, num=100)
x1 = []
y1 = []
for k in t:
    x = ((vel*k)*math.cos(math.radians(ang)))     
    y = ((vel*k)*math.sin(math.radians(ang)))-((0.5*9.8)*(k**2))
    x1.append(x)
    y1.append(y)
p = [i for i, j in enumerate(y1) if j < 0]
for i in sorted(p, reverse = True):
    del x1[i]
    del y1[i]

plt.xlabel("Distancia",fontsize=20,color="red")                                      
plt.ylabel("Altura",fontsize=20,color="blue")
ymax_label = "Ymax: " + str(round(ymax,2)) 
xmax_label = "Xmax: " + str(round(xmax,2)) 
plt.axhline(y=ymax,color = "red", linewidth = 1, linestyle = "dashed", label= ymax_label)
plt.axvline(x=xmax,color = "green", linewidth = 1, linestyle = "dashed", label= xmax_label)
plt.legend()
plt.grid("True")
plt.plot(x1, y1) 
plt.show()
