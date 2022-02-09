import os
from operator import itemgetter
from math import sqrt



def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros
    
def get_void_shape(x,y):
    shape = []
    for x in range(0,x):
        shape.append(zerolistmaker(y))
    return shape

def print_shape(shape):
    x = len(shape)
    y = len(shape[0])
    proceed_shape = get_void_shape(y,x)
    for i in range(x):
        for j in range(y):
            proceed_shape[j][i] = str(shape[i][j])
    for j in range(y):
        L = "".join(proceed_shape[j])
        print(L)

def distance(coord_a,coord_b):
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return sqrt((xb-xa)**2+(yb-ya)**2)
    

def squareFinding(image,x_len = 0,y_len = 0):
    shapes = []
    for x in range(x_len):
        for y in range(y_len):
            if image[x][y] == 1:
                shape = get_void_shape(x_len,y_len)
                shape[x][y] = 1
                image[x][y] = 0
                #adding first colored pixel
                #looking for the next connected one
                keepLooking = True
                while keepLooking:
                    keepLooking = False
                    for i in -1,0,1:
                        for j in -1,0,1:
                            try:
                                if image[x+j][y+i] == 1:
                                    keepLooking = True 
                                    x = x + j
                                    y = y + i
                                    
                                    shape[x][y] = 1
                                    image[x][y] = 0   
                            except IndexError:
                                pass
                shapes.append(shape)
    for shape in shapes:
        print_shape(shape)
        print('\n')

    results = []
    for shape in shapes:
        test1 = False
        test2 = False
        coords = []
        for x in range(x_len):
            for y in range(y_len):
                if shape[x][y] == 1:
                    coord = [x,y]
                    coords.append(coord)
                    
                    
                    
        if len(coords) > 4:
            coords = sorted(coords, key=itemgetter(0))
            
            x_max = coords[-1]
            x_min = coords[0]
            
            coords = sorted(coords, key=itemgetter(0))
            
            y_max = coords[-1]
            y_min = coords[0]
            
            x_dist = distance(x_max,x_min)
            y_dist = distance(y_max,y_min)
            
            error = ((x_dist-y_dist)/x_dist) * 100
            if error < 10:
                test1 = True 
                print('test1')
                
            Vx = [(x_max[0]+x_min[0])/2,(x_max[1]+x_min[1])/2]
            Vy = [(y_max[0]+y_min[0])/2,(y_max[1]-y_min[1])/2]
            O = [(Vx[0] + Vy[0])/2,(Vx[1] + Vy[1])/2]
            
            
            X = []
            Y = []
            for coord in coords:
                X.append(coord[0])
                Y.append(coord[0])
                
            M = [sum(X)/len(X),sum(Y)/len(Y)]
            
            if M[0] > O[0]*0.9 and M[0] < O[0]*1.1 and M[1] > O[1]*0.9 and M[1] < O[1]*1.1:
                test2 = True 
            
            if test1 and test2:
                return [M]
            if test1 or test2:
                results.append(M)
    return results
        
                        
if __name__ == '__main__':
    y = 0
    x = 0
    image = []
    file = open('image.py','r')
    for ligne in file:
        image.append([])
        x = 0
        for char in ligne:
            x += 1
            if char != '\n' and char != ' ':
                image[y].append(int(char))
        y += 1
    x = x - 1
    y = len(image)
    proceed_image = get_void_shape(x,y)
    for j in range(y):
        for i in range(x):
            proceed_image[i][j] = image[j][i]
    print(squareFinding(proceed_image,x,y))
