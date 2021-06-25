import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import asyncio
from os import walk
import math
from matplotlib import pyplot

point = [515000, 6220000]
ecart = 25
angle = 1
horizon = 30000

list_obs = []

async def get_points(angle, centre, ecart, horizon, map):
    local_max = 0
    coord_max = centre
    counter = 0
    marked = True
    rad = math.radians(angle)
    for dist in range(ecart, horizon, ecart):
        p = (centre[0] + math.cos(rad) * dist, centre[1] + math.sin(rad) * dist)
        value = next(map.sample([p], masked=True))[0]
        if value > local_max:
            local_max = value
            coord_max = p
            marked = True
        elif counter > 200 and marked:
            marked = False
            counter = 0
            list_obs.append(coord_max)
        else:
            counter += 1

#filenames = next(walk('bd_alti'), (None, None, []))[2]
#tot_map = []
#
#for f in filenames:
#    if math.sqrt((int(f[17:21]) + 12.5 - (point[0] / 1000))**2  + (int(f[22:26]) - 12.5 - (point[1] / 1000))**2) < horizon / 1000 + 25:
#        src = rasterio.open('bd_alti/' + f)
#        tot_map.append(src)
#
#temp, out_trans = merge(tot_map, nodata=0)

temp = rasterio.open('mns_france.tif')


for i in range(0, 360, angle):
    asyncio.run(get_points(i, point, ecart, horizon, temp))


pyplot.imshow(temp.read(1), extent=(temp.bounds.left, temp.bounds.right, temp.bounds.bottom, temp.bounds.top))
pyplot.scatter(*zip(*list_obs), linewidths=0.1, marker='.', c='red')
pyplot.show()
#print(temp.bounds[0])
#print(temp)
#show(temp, cmap='terrain')