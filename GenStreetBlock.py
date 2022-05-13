import bpy
import numpy as np
from perlin_noise import PerlinNoise
import random
# make collection
new_collection = None

def makeBox(ori,xHalfLen,yHalfLen,zHalfLen): 
    # make mesh
    vertices = []
    cnt=0
    for x in (1,-1):
        for y in (1,-1):
            for z in (1,-1):  
                if (cnt==13):
                    break
                    #pass
                vx=np.array([x,y,z])
                vx = vx* np.array([xHalfLen,yHalfLen,zHalfLen])
                vx = ori + vx
                vertices.append(vx)
                cnt = cnt + 1
                
                 
    faces = [(1,2,6,5),(3,4,8,7),(5,6,8,7),(1,2,4,3),(1,3,7,5),(2,4,8,6)]
    faces = [(0,1,5,4),(2,3,7,6),(4,5,7,6),(0,1,3,2),(0,2,6,4),(1,3,7,5)]
    #faces = [(1,2,3)]
    #faces = [(0,1,2)]
    #faces = []
    
    #edges = [(1,2),(1,3),(4,2),(4,3),(5,6),(5,7),(8,6),(8,7),(3,4),(3,7),(8,4),(8,7),(1,2),(1,5),(6,2),(6,5),(1,3),(1,5),(7,3),(7,5),(2,4),(2,6),(8,4),(8,6)]
    #edges = [(1,2)]
    edges = []
    
    new_mesh = bpy.data.meshes.new('new_mesh')
    new_mesh.from_pydata(vertices, edges, faces)
    new_mesh.update() 
    new_object = bpy.data.objects.new('new_object', new_mesh) 
    new_collection.objects.link(new_object)  
print("hi")

vori=np.array([50,50,50])

for collection in bpy.data.collections:
   #print(collection.name)
   if (collection.name == "CollPy"):
       new_collection=collection  
       
noise = PerlinNoise()
def fbm(st): 
    value = 0.0;
    amplitude = .5;
    frequency = 3.;
    
    for i in range(0,6): 
        value += amplitude * noise(st * frequency);
        frequency *= 2;
        amplitude *= 0.78; 
    return value;

rowLen=100
rowCnt=80
postr=np.array([0,0,0])-np.array([rowLen*rowCnt/2,rowLen*rowCnt/2,0])

cropu=[]
cropv=[]
for i in range(0,int(rowCnt*1/2)):
    u=int(random.random()*rowCnt)
    v=int(random.random()*rowCnt)
    cropu.append(u)
    cropv.append(v)
    
    
for i in range(0,rowCnt):
    for k in range(0,rowCnt):
        posn=postr + np.array([i*rowLen,k*rowLen,0])
        
        noii=i/rowCnt
        noik=k/rowCnt
        
        #noix=noise([noii,noik])
        noix=fbm(np.array([noii,noik]))
        
        '''
        if (noix < -0.1):
            continue
        if (random.random()<0.5):
            continue;
        '''
        
        if ((i in cropv) or (k in cropu)):
            continue
        
        noix=(noix+1)/2
        print(noix)
        noix = noix * 5000
        makeBox(posn,50,50,noix)