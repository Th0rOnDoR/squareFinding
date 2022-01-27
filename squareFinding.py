import os
from operator import itemgetter
from math import sqrt
from tabulate import tabulate



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
    print('')

def distance(coord_a,coord_b):
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return sqrt((xb-xa)**2+(yb-ya)**2)



def squareFinding(captchaPath):
    
    """
    extract captcha from file
    """
    
    y = 0
    x = 0
    image = []
    decalage_x = 0
    decalage_x_fin = 0
    end_decalage = False
    y_ligne = []
    file = open(captchaPath,'r')
    for ligne in file:
        y_ligne = []
        x = 0
        s = 0
        for char in ligne:
            if char != '\n' and char != ' ':
                s += int(char)
                x += 1
                y_ligne.append(int(char))
        if s <15:
            image.append(y_ligne)
            end_decalage = True
        elif not end_decalage:
            decalage_x_fin += 1
        else:
            decalage_x += 1
        y += 1
    y = len(image)
    x_len = x
    y_len = y
    proceed_image = get_void_shape(x,y)
    for j in range(y):
        for i in range(x):
            proceed_image[i][j] = image[j][i]


    """
    then extracting every shapen from captcha
    """

    x = 0
    y = 0
    shapes = []
    for x in range(x_len):
        for y in range(y_len):
            if proceed_image[x][y] == 1:
                branch = []
                shape = get_void_shape(x_len,y_len)
                shape[x][y] = 1
                proceed_image[x][y] = 0
                #adding first colored pixel
                #looking for the next connected one
                keepLooking = True
                while keepLooking:
                    keepLooking = False
                    for i in -1,0,1:
                        for j in -1,0,1:
                            try:
                                if proceed_image[x+j][y+i] == 1:
                                    keepLooking = True
                                    dx = x + j
                                    dy = y + i
                                    branch.append([dx,dy])
                            except IndexError:
                                pass
                    if not keepLooking:
                        for i in -2,-1,0,1,2:
                            for j in -2,-1,0,1,2:
                                try:
                                    if proceed_image[x+j][y+i] == 1:
                                        keepLooking = True
                                        dx = x + j
                                        dy = y + i
                                        branch.append([dx,dy])
                                except IndexError:
                                    pass
                    if branch.__len__() != 0:
                        keepLooking = True
                        dx = branch[0][0]
                        dy = branch[0][1]
                        branch.remove([dx,dy])
                        shape[dx][dy] = 1
                        proceed_image[dx][dy] = 0
                        x = dx
                        y = dy    
                shapes.append(shape)
       
                         
    """
    priting everyshape
    for debug*
    """
    
    #for shape in shapes:
        #print_shape(shape)
        #print('\n')
    #print(len(shapes))
    
    
    
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
                    
                    
                    
        if len(coords) > 20:
            
            """
            first test, check if diagonals have the same dist and if there is four point 
            """
            coords = sorted(coords, key=itemgetter(0))
            x_max = coords[-1]
            x_min = coords[0]
            coords = sorted(coords, key=itemgetter(1))
            y_max = coords[-1]
            y_min = coords[0]
            x_dist = distance(x_max,x_min)
            y_dist = distance(y_max,y_min)

            error = abs(x_dist/y_dist)*100
            print(error)
            if error < 110 and error > 90 and x_max != y_max != x_min != y_min:
                test1 = True
                print('test1')
                
                
            
            
            """
            second test, check if center of shape == center of diagonals
            """
            Vx = [(x_max[0]+x_min[0])/2,(x_max[1]+x_min[1])/2]
            Vy = [(y_max[0]+y_min[0])/2,(y_max[1]+y_min[1])/2]
            O = [(Vx[0] + Vy[0])/2,(Vx[1] + Vy[1])/2]
            
            #print(x_max)
            #print(x_min)
            shape[int(x_max[0])][int(x_max[1])] = 'X'
            shape[int(x_min[0])][int(x_min[1])] = 'x'
            #print(y_max)
            #print(y_min)
            shape[int(y_max[0])][int(y_max[1])] = 'Y'
            shape[int(y_min[0])][int(y_min[1])] = 'y'
            #print(Vx)
            #print(Vy)
            shape[int(Vx[0])][int(Vx[1])] = 'v'
            shape[int(Vy[0])][int(Vy[1])] = 'V'
            
            X = []
            Y = []
            for coord in coords:
                X.append(coord[0])
                Y.append(coord[1])

            M = [(sum(X)/len(X)),sum(Y)/len(Y)]
            
            print(O)
            print(M)
            shape[int(M[0])][int(M[1])] = 2
            shape[int(O[0])][int(O[1])] = 3
            
            print_shape(shape)
            
            
            if M[0] > O[0]*0.975 and M[0] < O[0]*1.025 and M[1] > O[1]*0.975 and M[1] < O[1]*1.025:
                test2 = True
                print('test 2')
                
                
            for result in results:
                
                
                k = result[1]
                result[1] = result[0]
                result[0] = abs(-270 + k + decalage_x)
                
            if test1 and test2:
                return [M]
            if test1 or test2:
                results.append(M)
    return results
    
def main():
    pass


if __name__ == '__main__':
    #print(squareFinding("image2.py"))
    print(squareFinding("original.py"))
