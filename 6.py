import os
from operator import itemgetter
from math import sqrt
#from tabulate import tabulate
import datetime
from math import acos
from math import pi

def distance(coord_a,coord_b):
    """retun distance between two points"""
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return sqrt((xb-xa)**2+(yb-ya)**2)

def distanceSquare(coord_a,coord_b):
    """
    retun square distance between two points,
    we dont need to dind the square to guess if two lines are almost egal
    """
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return (xb-xa)**2+(yb-ya)**2

def angle(b,c,a):
    """returns the angle (in degrees) of the angle BAC"""
    alpha = (b*b + c*c - a*a)/(2*b*c)
    if alpha <= 1 and alpha > -1:
        return (acos(alpha))*180/pi
    else:
        return -1
    
def scalar(a,b):
    """scalar of two vectors"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    return xa*xb + ya*yb

def almostEgalPoint(a,b):
    """return True if the point are almost egal, image isnt in HD so 0,1 or 1, whats the matter ?"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    dx = abs(xa - xb)
    dy = abs(ya - yb)
    if dx < 5 or dy < 5:
        return True
    return False


def almostEgalPoint2(a,b):
    """return True if the point are almost egal, image isnt in HD so 0,1 or 1, whats the matter ?"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    dx = abs(xa - xb)
    dy = abs(ya - yb)
    if dx < 2 or dy < 2:
        return True
    return False
    
    
def almostEgalDistance(a,b):
    """same but for distance/number"""
    if a > 0.95*b and a < 1.05*b:
        return True
    return False

def zerolistmaker(n):
    """Utility fonction to create void shape"""
    listofzeros = [0] * n
    return listofzeros

def getVoidShape(x,y):
    """create an void image by adding list of 0"""
    shape = []
    for x in range(0,x):
        shape.append(zerolistmaker(y))
    return shape
    
    

def printShape(shape):
    """print shape, the default print() return the list so, for debug, show a shape an human can understand"""
    x = len(shape)
    y = len(shape[0])
    proceed_shape = getVoidShape(y,x) #getting a void image
    for i in range(x):
        for j in range(y):
            if str(shape[i][j]) == '0':   #changing for every value of the shape 0 to single quote, its 
                proceed_shape[j][i] = "'" #easier to understand than a full shape of 0 and 1
            else:
                proceed_shape[j][i] = str(shape[i][j]) #We do not touch to others values 
                #we rotate x and y to, else the shape would be to big to be show 
    #now, the shape is proceed, lets print it
    for j in range(y): #for each line 
        L = "".join(proceed_shape[j]) #merge shape line by line
        #if L != "'"*40: to removd void
        print(L)
    print('') #to separate shape from next one

def middlePoint(p1,p2):
    return [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]

def isSquare(p1, p2, p3, p4, points):
    """ 
    Useful, test if p1,2,3 and 4 form a parallelogram, return True or False
    
    1st we try if 2 opposite segments are egal, if not, return false
    then, we the others opposite segments are egal, if not, false
    then, 
    """
    p1p2 = distanceSquare(p1, p2)
    p3p4 = distanceSquare(p3, p4)
    #inf 10^2, sup 30^2
    if almostEgalDistance(p1p2,p3p4) and p1p2 > 70 and p1p2 < 700:
        
        p1p4 = distanceSquare(p1, p4)
        p2p3 = distanceSquare(p2, p3)
        
        if almostEgalDistance(p1p4,p2p3) and p1p4 > 70 and p1p4 < 700:
            p2p4 = distanceSquare(p2, p4)
            p1p3 = distanceSquare(p1, p3)
            if p2p4 > p1p3/2 and p2p4 < p1p3*1.5:
                m = middlePoint(p1,p4)
                x = m[0]
                y = m[1]
                for point in points:
                    if almostEgalPoint2(m,point):
                        m = middlePoint(p2,p3)
                        x = m[0]
                        y = m[1]
                        for point in points:
                            if almostEgalPoint2(m,point):
                                m = middlePoint(p1,p2)
                                x = m[0]
                                y = m[1]
                                for point in points:
                                    if almostEgalPoint2(m,point):
                                        m = middlePoint(p3,p4)
                                        x = m[0]
                                        y = m[1]
                                        for point in points:
                                            if almostEgalPoint2(m,point):
                                                return True
                    
                        
                #if point in middle segment + ask optimisation
            #return True
            
            #60* -> 120 deg
            
    return False



def ExtractCaptchaFromFile(captchaPath):
    """
    We extract the captcha from the file, but, because the file is rotated, we rotate the captchq
    thats a terrible way lf doing this but, great, it work.
    
    First of all, until a line count less than 15 times 1, 
    we will considerer line are some kind of interferance, so we will remove them
    then, we know the caltcha is 240 pixel by 40 so, so we dont care about some interferance after x = 240
    
    """    
    y = 0
    x = 0
    image = []
    decalage_x = 0 #first interferance
    decalage_x_fin = 0 #last one 
    end_decalage = False # end of first interferance
    file = open(captchaPath,'r') #opening captcha
    for ligne in file: #for each line
        y_ligne = [] #the line y
        x = 0
        s = 0
        for char in ligne: #for every char exept void or \n, adding it to y_ligne 
            if char != '\n' and char != ' ':
                s += int(char)
                x += 1 #counting number of x
                y_ligne.append(int(char))
        if s <15 and image.__len__() <= 240:
            image.append(y_ligne) #if ligne isnt in first interferance or last interferance
            end_decalage = True #adding it to the image
        elif not end_decalage: #first interferance
            decalage_x += 1
        else: #last interferance
            decalage_x_fin += 1
                
    
    y = len(image) #getting dimension
    proceed_image = getVoidShape(x,y)
    for j in range(y):
        for i in range(x):
            proceed_image[i][j] = image[j][i] #rotate the image
    #printShape(proceed_image)
    #print(decalage_x)
    return proceed_image, decalage_x, x, y
    
def ExtractShapesFromCaptcha(proceed_image,x_len,y_len):
    """
    then extracting every shape from captcha
    we first look for a colored pixel, the  the next one 
    when there is no next one, we stop and make another shape
    """
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
                    keepLooking = False #we wont find anything and i need to spot the loop si
                    for i in -1,0,1: #for every pixel next to the first one
                        for j in -1,0,1:
                            try:
                                if proceed_image[x+j][y+i] == 1 and x+j >= 0 and y+i >= 0:
                                    #x+j>= 0 because -1 take the last element 
                                    keepLooking = True
                                    dx = x + j
                                    dy = y + i
                                    if not [dx,dy] in branch: #to avoid a point to be add 15 times
                                        branch.append([dx,dy]) #if there is more than one point 
                                    shape[dx][dy] = 1 #next to the first one, then we remove detect points 
                                    proceed_image[dx][dy] = 0 # and we add then to the new shape
                            except IndexError: #yea, 0 - 1 = -1 
                                pass
                    if not keepLooking: #same thing but with a bigger radius
                        for i in -2,-1,0,1,2: #maybe there is a hole so
                            for j in -2,-1,0,1,2:
                                try:
                                    if proceed_image[x+j][y+i] == 1:
                                        keepLooking = True
                                        dx = x + j
                                        dy = y + i
                                        if not [dx,dy] in branch:
                                            branch.append([dx,dy])
                                        shape[dx][dy] = 1
                                        proceed_image[dx][dy] = 0
                                except IndexError:
                                    pass
                    
                    if not keepLooking: #could be a big hold
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
                    if branch.__len__() > 500: #to avoid infinite loop
                        shape = proceed_image
                        printShape(proceed_image)
                        break
                shapes.append(shape)
                #printShape(shape)
    return shapes, x_len, y_len










def squareFinding(captchaPath):
    """
    return pos x,y of the square in the original captcha
    """
    time1 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S") 
    
    proceed_image, decalage_x,x_len,y_len = ExtractCaptchaFromFile(captchaPath)
    shapes, x_len, y_len = ExtractShapesFromCaptcha(proceed_image,x_len,y_len)
                         
    """
    priting everyshape
    for debug*
    """
    
    #for shape in shapes:
        #printShape(shape)
        #print('\n')
    #print(len(shapes))
    #print('oui')
    
    results = [] #the result 
    
    
    for shape in shapes:
        #for each shape
        coords = [] #coords of every pixel being one
        for x in range(x_len):
            for y in range(y_len):
                if shape[x][y] == 1:
                    coord = [x,y]
                    coords.append(coord)
        
        #if len(coords) > 50 and len(coords) < 200:
        if len(coords) > 60: #id there is less than 60px colored, it wont be a square
            a = 0
            #d = 0
            
            coords = sorted(coords, key=itemgetter(0)) #we want to sort the list to get a extreme point
            x_max = coords[-1] #this point is an angle for sure
            
            shape[int(x_max[0])][int(x_max[1])] = 'X'
            #printShape(shape)
            #for debug
            
            
            for i in coords:
                #b = 0
                #a += 1
                
                for j in coords:
                    #b += 1
                    #c = 0
                    for k in coords:
                        #c += 1
                        #print(len(coords),a,b,c,d) #for debug too, slow down everything
                        if not almostEgalPoint(i,j) and not almostEgalPoint(j,k) and not almostEgalPoint(k,x_max) and not almostEgalPoint(x_max,i): #if there are almost egal
                            #the result will be wrong so...
                            if isSquare(i,j,k,x_max,coords): #if is square
                                O = [(i[0]+j[0]+k[0]+x_max[0])/4,(i[1]+j[1]+k[1]+x_max[1])/4]
                                #d += 1 #adding the center to result if he's not alrrady in it
                                try:
                                    #print(results[-1])
                                    #print(O)
                                    if not almostEgalPoint(results[-1],O):
                                        results.append(O)
                                except IndexError:
                                    #pass
                                    results.append(O)
                                #results.append(O)
                                
    """
    now lets edit the results, because there is more than one point and
    there are in relative coords (without interferance from beginning)
    """
    r = [] #the result we will return
    Y = [] #list of all Y coords
    X = [] #list of all X coords
    
    try: #results could be None so..
        for result in results:
            Y.append(result[1])
            X.append(result[0])
            
            
        M = [(sum(X)/len(X)),sum(Y)/len(Y)]   #center point of all square 
          
        for result in results:
            r.append([distance(result,M),result]) 
        r = sorted(r, key=itemgetter(1)) #we take the square near to the center 
        time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        print(time1)
        print(time2)
        #return r
        r = r[0][1] #and we return it 
        return r[1]+decalage_x+5,r[0]+5 #with interferance, and +5 because the detected square are not almost equal and it could be a quare a bit too much up the square
        
        
    except ZeroDivisionError:
        time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        print(time1)
        print(time2)
        return  
        
