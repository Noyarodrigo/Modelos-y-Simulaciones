import math
import numpy as np
import matplotlib.pylab as plt
import random

anotaciones = True

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


#repetir 10 veces
curvas_x = []
curvas_y = []

for i in range(10):
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
    n_dist_2m = 0
    o_dist_2m = 0
    xtmp = []
    ytmp = []

    while y >= 0 :
        #va sumando puntos para representar después, son las formulas de arriba
        x = ((velx*dt)*math.cos(math.radians(ang)))
        y = ((vel*dt)*math.sin(math.radians(ang)))-((0.5*9.8)*(dt**2))
        xtmp.append(x)
        ytmp.append(y)

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

        #se fija si está dentro de la rafaga de viento
        #clase 13/04/21
        #   se agrega que esté dentro del intervalo de +-1% o
        #   que el último valor sea el más próximo a 2 metros
        if (y >= hmin and y <= hmax) or distprox_2m == True:
            if flag_acelerado == False:
                #El proyectil encontró una rafaga de aire
                randomito = random.random()
                punto_cambio.append(contador)

                #no hace nada >30%
                if randomito < prob_rafaga:
                    #print('No hace nada...')
                    pass
                #acelera 33-66%
                if randomito >= prob_rafaga and randomito <= prob_rafaga*2:
                    #print('Se aceleró')
                    velx = velx+1
                    #print(f'velx: {velx}')
                    flag_distinto = True
                #frenado <66%
                if randomito > prob_rafaga*2:
                    #print('Se frenó')
                    velx = velx-2
                    #print(f'velx: {velx}')
                    flag_distinto = True

                flag_acelerado = True
        ultimo_y = y
        contador = contador + 1
        dt=dt+0.001
    curvas_x.append(xtmp)
    curvas_y.append(ytmp)
#parte matplot
colores = ['b','g','r','c','m','y','k']
plt.xlabel("Distancia",fontsize=20,color="red")
plt.ylabel("Altura",fontsize=20,color="blue")

#valores sin viento
plt.axhline(y=ymax,color = "red", linewidth = 1, linestyle = "dashed")
plt.axvline(x=xmax,color = "green", linewidth = 1, linestyle = "dashed")
plt.grid("True")

#parabola
for i in range(len(curvas_x)):
    plt.plot(curvas_x[i], curvas_y[i],color = colores[random.randint(0,6)], label = 'curva:'+str(i))

plt.legend()
plt.show()
