import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from os import walk
import math
from matplotlib import pyplot

point = [540000, 6240000]
ecart = 1000
angle = 5
distance = 30000

list_obs = []

for i in range(0, 360, angle):
    rad = 2 * 3.141592 * i / 360
    for j in range(ecart, distance, ecart):
        list_obs.append((point[0] + math.cos(rad) * j,point[1] + math.sin(rad) * j))


filenames = next(walk('bd_alti'), (None, None, []))[2]
tot_map = []

for f in filenames:
    if math.sqrt((int(f[17:21]) + 12.5 - (point[0] / 1000))**2  + (int(f[22:26]) - 12.5 - (point[1] / 1000))**2) < distance / 1000 + 25:
        src = rasterio.open('bd_alti/' + f)
        tot_map.append(src)

temp, out_trans = merge(tot_map, nodata=0)

#pts = [x for x in temp.sample(list_obs)]
pyplot.imshow(temp[0], extent=(499987.5, 574987.5, 6200012.5, 6275012.5))
pyplot.scatter(*zip(*list_obs), linewidths=0.1, marker='.', c='red')
pyplot.show()
#print(temp.bounds[0])
#print(temp)
#show(temp, cmap='terrain')