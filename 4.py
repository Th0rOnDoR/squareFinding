import os
from operator import itemgetter
from math import sqrt
#from tabulate import tabulate
import datetime

def scalar(a,b):
    """scalar of two vectors"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    return xa*xb + ya*yb

def almostEgalPoint(a,b):
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    dx = abs(xa - xb)
    dy = abs(ya - yb)
    if dx < 4 or dy < 4:
        return True
    return False

def almostEgalDistance(a,b):
    if a > 0.95*b and a < 1.05*b:
        return True
    return False

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def getVoidShape(x,y):
    shape = []
    for x in range(0,x):
        shape.append(zerolistmaker(y))
    return shape

def printShape(shape):
    x = len(shape)
    y = len(shape[0])
    proceed_shape = getVoidShape(y,x)
    for i in range(x):
        for j in range(y):
            if str(shape[i][j]) == '0':
                proceed_shape[j][i] = "'"
            else:
                
                proceed_shape[j][i] = str(shape[i][j])
    for j in range(y):
        L = "".join(proceed_shape[j])
        #if L != '                                        ':
        print(L)
    print('')

def distance(coord_a,coord_b):
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return sqrt((xb-xa)**2+(yb-ya)**2)

def isSquare(p1, p2, p3, p4):

    p1p2 = distance(p1, p2)
    p1p3 = distance(p1, p3)
    p1p4 = distance(p1, p4)
    p2p3 = distance(p2, p3)
    p2p4 = distance(p2, p4)
    p3p4 = distance(p3, p4)
    if p1p2 < 10 or p1p4 < 10 or p2p3 < 10 or p1p3 < 14 or p2p4 < 14 or p3p4 < 10:
        return False
    if p1p2 > 30 or p1p4 > 30 or p2p3 > 30 or p3p4 > 30:
        return False
    #p1p2 = p3p4 and p2p3 = p1p4
    if almostEgalDistance(p1p2,p3p4) and almostEgalDistance(p1p3,p2p4):
        return True
    return False



def ExtractCaptchaFromFile(captchaPath):
        
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
        if s <15 and image.__len__() <= 240:
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
    proceed_image = getVoidShape(x,y)
    for j in range(y):
        for i in range(x):
            proceed_image[i][j] = image[j][i]
    return proceed_image, decalage_x, x_len, y_len
    
def ExtractShapesFromCaptcha(proceed_image,x_len,y_len):
    """
    then extracting every shape from captcha
    """
    k = True
    #printShape(proceed_image)
    x = 0
    y = 0
    shapes = []
    for x in range(x_len):
        for y in range(y_len):
            if proceed_image[x][y] == 1:
                #print('new shape')
                branch = []
                shape = getVoidShape(x_len,y_len)
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
                                if proceed_image[x+j][y+i] == 1 and x+j > 0 and y+i > 0:
                                    keepLooking = True
                                    dx = x + j
                                    dy = y + i
                                    if not [dx,dy] in branch:
                                        branch.append([dx,dy])
                                    shape[dx][dy] = 1
                                    proceed_image[dx][dy] = 0
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
                                        #if not [dx,dy] in branch:
                                        branch.append([dx,dy])
                                        shape[dx][dy] = 1
                                        proceed_image[dx][dy] = 0
                                except IndexError:
                                    pass
                    if not keepLooking:
                        for i in -3,-2,-1,0,1,2,3:
                            for j in -3,-2,-1,0,1,2,3:
                                try:
                                    if proceed_image[x+j][y+i] == 1:
                                        keepLooking = True
                                        dx = x + j
                                        dy = y + i
                                        #if not [dx,dy] in branch:
                                        branch.append([dx,dy])
                                        shape[dx][dy] = 1
                                        proceed_image[dx][dy] = 0
                                except IndexError:
                                    pass                
                    if branch.__len__() != 0:
                        #print(branch.__len__())
                        keepLooking = True
                        dx = branch[0][0]
                        dy = branch[0][1]
                        
                        branch.remove([dx,dy])
                        #print(branch)
                        #print(dx, dy)
                        x = dx
                        y = dy    
                    if branch.__len__() > 500 and k:
                        #printShape(proceed_image)
                        #printShape(shape)
                        return None
                shapes.append(shape)
                #printShape(shape)
    return shapes, x_len, y_len










def squareFinding(captchaPath):
    proceed_image, decalage_x,x_len,y_len = ExtractCaptchaFromFile(captchaPath)
    shapes, x_len, y_len = ExtractShapesFromCaptcha(proceed_image,x_len,y_len)
                         
    '''
    priting everyshape
    for debug*
    '''
    
    #for shape in shapes:
        #printShape(shape)
        #print('\n')
    #print(len(shapes))
    #print('oui')
    
    results = []
    time1 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    
    for shape in shapes:
        
        coords = []
        for x in range(x_len):
            for y in range(y_len):
                if shape[x][y] == 1:
                    coord = [x,y]
                    coords.append(coord)
        
        if len(coords) > 50 and len(coords) < 200:
            a = 0
            d = 0
            
            coords = sorted(coords, key=itemgetter(0))
            x_max = coords[-1]
            
            
            
            
            for i in coords:
                #b = 0
                #a += 1
                
                for j in coords:
                    #b += 1
                    #c = 0
                    for k in coords:
                        #c += 1
                        #print(len(coords),a,b,c,d)
                        if not almostEgalPoint(i,j) and not almostEgalPoint(j,k) and not almostEgalPoint(k,x_max) and not almostEgalPoint(x_max,i):
                            if isSquare(i,j,k,x_max):
                                O = [(i[0]+j[0]+k[0]+x_max[0])/4,(i[1]+j[1]+k[1]+x_max[1])/4]
                                d += 1
                                #try:
                                    #if not almostEgalPoint(results [-1],O):
                                        #results.append(O)
                                #except IndexError:
                                    #results.append(O)
                                results.append(O)
    r = []
    Y = []
    X = []
    for result in results:
        Y.append(result[1])
        X.append(result[0])
    M = [(sum(X)/len(X)),sum(Y)/len(Y)]                     
    for result in results:
        r.append([distance(result,M),result])
    r = sorted(r, key=itemgetter(1))
    time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    print(time1)
    print(time2)
    r = r[0][1]
    return r[1]+(270-decalage_x-240)+5,r[0]+5
                                
            
            
            
            
if __name__ == '__main__':
    '''
    for i in range(1,12):
        name = 'captcha/' + str(i)+'.txt'
        print(squareFinding(name))
        print(i)
        print('')
        print('')
    '''
    print(squareFinding("captcha/14.txt"))
    
