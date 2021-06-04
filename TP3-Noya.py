import math
import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import random

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


curvas_x = []
curvas_y = []
curvas_z = []
ultimos_puntos = []

for i in range(iteraciones):
    #print('Tirada:',i)
    #variables para saber si cambio la distancia y/o altura y graficar despues
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
    n_dist_2m = 0
    o_dist_2m = 0
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

        #nuevo line altura max
        if y > ultimo_y_max:
            ultimo_y_max = y

        #clase 13/04/21
        # se agrega la dltima distancia más próxima a 2 metros para después
        n_dist_2m = abs(2 - ultimo_y)
        o_dist_2m = abs(2 - y)
        if n_dist_2m < o_dist_2m and distprox_2m == False:
            distprox_2m = True
            #print(n_dist_2m)

        #nueva oportunidad: si paso la mitad esta en caida y reinicia el flag
        if y < ultimo_y and flag_caida == False:
            #print('Ahora está en caida')
            flag_caida = True
            flag_acelerado = False
            y_caida = ultimo_y
            distprox_2m = False

        if (y >= hmin and y <= hmax) or distprox_2m == True:
            if flag_acelerado == False:
                #print('El proyectil encontró una rafaga de aire')
                randomito = random.random()
                punto_cambio.append(contador)

                #aparece viento >49%
                if randomito >= 0.5:
                    vel_viento = random.uniform(0,8)
                    ang_viento = random.randint(0,359)
                    velx = velx + math.cos(ang_viento) * vel_viento
                    velz = velz + math.sin(ang_viento) * vel_viento
                    flag_distinto = True

                flag_acelerado = True
        ultimo_y = y
        contador = contador + 1
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
ax1.set(xlabel="Distancia", ylabel="Altura")
ax2.set(xlabel="Desviación Z", ylabel="Distancia X")
ax3.set(xlabel="Desviación Z", ylabel="Distancia X")
#parabola
for i in range(len(curvas_x)):
    ax1.plot(curvas_x[i], curvas_y[i],color = colores[random.randint(0,6)])
    ax2.plot(curvas_z[i], curvas_x[i],color = colores[random.randint(0,6)])
    circulo = plt.Circle((ultimos_puntos[i][1],ultimos_puntos[i][0]), 1, color = 'black')
    ax3.add_artist(circulo)

ax3.set_xlim([-45,45])
#plt.legend()
plt.show()
