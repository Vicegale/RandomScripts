from PIL import Image
import random

#Crates a Voronoi diagram

def distance(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def getClosest(points, x):
    closest = None
    minimumDist = 99999999999999999
    for i in points:
        d = distance(i[0], x)
        if d < minimumDist:
            minimumDist = d
            closest = i
    #print("----------")
    #print(x, closest, minimumDist)
    return closest
    
img = Image.new('RGB', (1920, 1080))

#Generate points
nPoints = 10
points = []
for i in range(nPoints):
    x = random.randint(0, img.size[0])
    y = random.randint(0, img.size[1])
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    points.append(((x, y), (r, g, b)))

print(points)    
pixels = img.load()
for i in range(0, img.size[0]):
    for j in range(0, img.size[1]):
        p = getClosest(points, (i, j))
        pixels[i, j] = p[1]
img.save("image.png", "PNG")
