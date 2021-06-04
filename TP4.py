#!/usr/bin/env python
# coding: utf-8

import math
import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import random
from scipy import stats

anotaciones = False

iteraciones = 100

h_rafaga = 2
tolerancia = 0.01
prob_rafaga = 0.33
hmax = h_rafaga * (1+tolerancia)
hmin = h_rafaga * (1-tolerancia)
flag_acelerado = False
flag_caida = False
flag_distinto = False

doc = str(input('Ingrese su doc:')).replace("0","1",4)
vel,ang = int(doc[:2]), int(doc[2:4])
velx = vel

#Xmax = vo**2 . sen(2 ang)/g
#Ymax = vo**2 . sen**2(ang)/2g

xmax = ((vel**2)/9.8) * math.sin(math.radians(2*ang))
ymax = ((vel**2) * math.pow(math.sin(math.radians(ang)),2))/(2*9.8)
tpo_vuelo = 2*vel*math.sin(math.radians(ang))/9.8

#tpo_vuelo = 2 .vo .sen ang /g
#x = vox.t con vox la vel por cos y lo mismo para y pero se agrega 1/2 grav y tpo cuad y se usa sin
#y = voy + 1/2 . g .t^2

velym = vel * math.sin(math.radians(ang))
velxm = vel * math.cos(math.radians(ang))

#para mas info poner en true anotaciones (arriba)
if anotaciones:
    print('vel:{}m/s, ang:{}°'.format(vel,ang))
    print(f'velx:{velxm:.2f}m/s, vely:{velym:.2f}m/s')
    print(f"Xmax: {xmax:.2f}m\nYmax: {ymax:.2f}m")
    print(f"Tiempo de vuelo: {tpo_vuelo:.2f}seg")


#-------------Dist. NORMAL VIENTO-------------
#para las bandas se toma el max val de Y y se lo
#redondea hacia arriba

bandas = int((math.ceil(ymax)))

mu = ymax
std_dev = mu/2

probs = []
for i in range(bandas+1):
    p = stats.norm.cdf(i, mu, std_dev)
    probs.append(p)

#cuando se llega a la mitad se tiene un poco más de
#50%, esto es por redondear ya que se pasa de mu
#---------------------------------------------

curvas_x = []
curvas_y = []
curvas_z = []
ultimos_puntos = []
vels = []
angs = []
for i in range(iteraciones):
    velx = vel
    y_caida = 0
    ultimo_y_max = 0
    ultimo_x_max = 0
    ultimo_y = 0
    punto_cambio = []
    contador = 0
    distprox_2m = False
    flag_caida = False
    flag_acelerado = False
    dt = 0
    y = 0
    x = 0
    z = 0
    velz = 0
    xtmp = []
    ytmp = []
    ztmp = []
    ult_tmp = []
    while y >= 0 :
        #va sumando puntos para representar después, son las formulas de arriba
        x = ((velx*dt)*math.cos(math.radians(ang)))
        y = ((vel*dt)*math.sin(math.radians(ang)))-((0.5*9.8)*(dt**2))
        z = velz * dt
        xtmp.append(x)
        ytmp.append(y)
        ztmp.append(z)

        #nueva oportunidad: si paso la mitad esta en caida y reinicia el flag
        if y < ultimo_y and flag_caida == False:
            #print('Ahora está en caida')
            flag_caida = True
            flag_acelerado = False
            y_caida = ultimo_y

        #determinar en que intervalo está el paquete de semillas (en metros)
        #por ej 0-1m, 1-2m, 2-3m ,etc
        y_interval = math.ceil(y)

        #determinar si ya fue acelerado
        if flag_acelerado == False:
            #valor para comparar con la probabilidad
            randomito = random.random()
            #prob viento en ese intervalo
            if randomito <= probs[y_interval]:
                vel_viento = np.random.exponential(scale= 0.1439)*100
                #angulo del viento dist. normal, mu en 180 std_dev 90
                ang_viento = np.random.normal(180,90)
                velx = velx + math.cos(ang_viento) * vel_viento
                velz = velz + math.sin(ang_viento) * vel_viento
                #print(f"vel viento:{vel_viento}, ang:{ang_viento}")
                vels.append(vel_viento)
                angs.append(ang_viento)
            flag_acelerado = True
        ultimo_y = y
        dt=dt+0.001
    curvas_x.append(xtmp)
    curvas_y.append(ytmp)
    curvas_z.append(ztmp)

    ult_tmp.append(xtmp[-1])
    ult_tmp.append(ztmp[-1])
    ultimos_puntos.append(ult_tmp)

#parte matplot
gs = gridspec.GridSpec(2, 2)
ax1 = plt.subplot(gs[0, :])
ax2 = plt.subplot(gs[1,0])
ax3 = plt.subplot(gs[1,1],sharex = ax2, sharey = ax2)

ax1.set_title('Vista lateral')
ax2.set_title('Vista superior')
ax3.set_title('Impacto Semilla')

colores = ['g','b','r','c','m','y','k']
ax1.set(xlabel="Distancia X", ylabel="Altura Y")
ax2.set(xlabel="Desviación Z", ylabel="Distancia X")
ax3.set(xlabel="Desviación Z")#, ylabel="Distancia X")

#parabola
cotax = 0
cotaz = 0
for i in range(len(curvas_x)):
    ax1.plot(curvas_x[i], curvas_y[i],color = colores[random.randint(0,6)])
    ax2.plot(curvas_z[i], curvas_x[i],color = colores[random.randint(0,6)])
    circulo = plt.Circle((ultimos_puntos[i][1],ultimos_puntos[i][0]), 1, color = 'black')
    ax3.add_artist(circulo)

    #determinar cota para gráfico
    #x
    if ultimos_puntos[i][0] > cotax:
        cotax = ultimos_puntos[i][0]
    #z
    if ultimos_puntos[i][1] > cotaz:
        cotaz = ultimos_puntos[i][1]

print(cotax,cotaz)
ax3.set_xlim([-cotaz +1,cotaz +1])
ax3.set_ylim([-cotax +1,cotax +1])
plt.tight_layout()
plt.show()

#distribuciones de comprobación
gs2 = gridspec.GridSpec(2, 1)
ax21 = plt.subplot(gs2[0, 0])
ax22 = plt.subplot(gs2[1,0])
ax21.hist(vels, bins = 20)
ax22.hist(angs, bins = 20)
plt.show()
