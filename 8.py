import os
from operator import itemgetter
from math import sqrt
#from tabulate import tabulate
import datetime
from math import acos
from math import pi

def distance(coord_a,coord_b): #useless
    """return distance between two points"""
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return sqrt((xb-xa)**2+(yb-ya)**2)

def distanceSquare(coord_a,coord_b): #useless
    """
    return square distance between two points,
    we dont need to dind the square to guess if two lines are almost egal
    """
    xa = coord_a[0]
    ya = coord_a[1]
    xb = coord_b[0]
    yb = coord_b[1]
    return (xb-xa)**2+(yb-ya)**2

def angle(b,c,a): #useless
    """returns the angle (in degrees) of the angle BAC"""
    alpha = (b*b + c*c - a*a)/(2*b*c)
    if alpha <= 1 and alpha > -1:
        return (acos(alpha))*180/pi
    else:
        return -1

def vector(a,b): #useless
    """vector of two points"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    return[xb - xa,yb - ya]

def middlePoint(p1,p2):
    """return the middle between two points"""
    return [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]

def scalar(a,b): #useless
    """scalar of two vectors"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    return xa*xb + ya*yb

def almostEgalPoint(a,b,tolerance): #useless
    """return True if the point are almost egal, image isnt in HD so 0,1 or 1, whats the matter ?"""
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    #print(xa,xb,ya,yb)
    dx = (max(xa,xb) - min(xa,xb))
    dy = (max(ya,yb) - min(ya,yb))
    #print(dx,dy,tolerance)
    if dx < tolerance and dy < tolerance:
        return True
    return False
    
def almostEgalDistance(a,b): #useless
    """same but for distance/number"""
    if a > 0.95*b and a < 1.05*b:
        return True
    return False
    
def pointBelongToLine(point,equa): #useless
    """
    test if a point belongs to a line of equation 
    equa[1] x + equa[2] y + equa[2] = 0 <=> (ax+by+c = 0)
    """
    c = equa[0]*point[0] + equa[1]*point[1] + equa[2]
    if c < 1.5 and c > -1.5:
        return True
    return False
    
def zerolistmaker(n): #useless
    """Utility fonction to create void shape"""
    listofzeros = [0] * n
    return listofzeros

def getVoidShape(x,y): #useless
    """create an void image by adding list of 0"""
    shape = []
    for x in range(0,x):
        shape.append(zerolistmaker(y))
    return shape
    
def printShape(shape): #pretty useless
    """
    print shape, the default print() return the list so, 
    for debug, show a shape an human can understand
    """
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
    
def ExtractShapesFromCaptcha(proceed_image,x_len,y_len): #useless
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
                points_number = 0
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
                                    points_number += 1 #number of point, 
                            except IndexError: #yea, 0 - 1 = -1 
                                pass
                    if True: #points_number < 100: 
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
                                            points_number += 1
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
                                            points_number += 1
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



def GetSquares():
    results = []
    for file in os.listdir("square"):
        if file.endswith(".txt"):
            #print(os.path.join("square/", file))
            name = os.path.join("square/", file)
            #name = "square/" + str(q) + ".txt"
            square,a,x_len_square,y_len_square = ExtractCaptchaFromFile(name)
            coordsSquare = [] #coords of every pixel being one
            #print(x_len_square,y_len_square)
            for x in range(x_len_square):
                for y in range(y_len_square):
                    if square[x][y] == 1:
                        #print(x,y)
                        #square[x][y] = 'x'
                        coord = [x,y]
                        coordsSquare.append(coord)
                        
            coordsSquare = sorted(coordsSquare, key=itemgetter(1))
            #printShape(coordsSquare)
            #print(coordsSquare)
            cte = coordsSquare[0][0]
            for i in range(len(coordsSquare)):
                a = coordsSquare[i][0]
                b = coordsSquare[i][1]
                #print(coordsSquare[i])
                coordsSquare[i] = [a-cte,b]
            results.append(coordsSquare)
    return results



def removeDuplicatesFromSquare():
    list_squares = GetSquares()
    index = []
    i = 0
    r = []
    for i in range(len(list_squares)):
        if list_squares[i] not in r:
            r.append(list_squares[i])
        else:
            print(i)
    print(len(r),len(list_squares))
    print(i)
        

    
def squareFinding(captchaPath):
    """
    return pos x,y of the square in the original captcha
    """
    time1 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S") 
    proceed_image, decalage_x,x_len,y_len = ExtractCaptchaFromFile(captchaPath)
    #shapes, x_len, y_len = ExtractShapesFromCaptcha(proceed_image,x_len,y_len)
    squares = GetSquares()
    shape = proceed_image
    results = []
    captcha_number = 0
    for coordsSquare in squares:
        for x in range(x_len):
            for y in range(y_len):
                if shape[x][y] == 1:
                    good = 0
                    
                    for squarePoint in coordsSquare:
                        try:
                            if shape[x+squarePoint[0]][y+squarePoint[1]] == 1 and x+squarePoint[0] >= 0 and y+squarePoint[1] >= 0:
                                good += 1
                            else:
                                pass
                        except IndexError:
                            pass
                    
                    if good >= len(coordsSquare)*0.5:
                        #print(good, len(coordsSquare))
                        X = []
                        Y = []
                        for coord in coordsSquare:
                            X.append(coord[0])
                            Y.append(coord[1])
                        #print(good,len(coordsSquare))
                        M = [(sum(X)/len(X))+x,sum(Y)/len(Y)+y,good/len(coordsSquare),captcha_number+1]
                        results.append(M)
        captcha_number += 1
        #return results
    r = [] #the result we will return
    #print(coords)
    try: #results could be None so..
        for result in results:
            r.append(result) 
        #print(r)
        #print(results)
        r = sorted(r, key=itemgetter(2)) #we take the square near to the center 
        time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        #print(time1)
        #print(time2)
        #return r
        r = r[-1] #and we return it 
        final_x = int(r[1]) + decalage_x
        final_y = int(r[0])
        return final_x,final_y #with interferance, and +5 because the detected square are not almost equal and it could be a quare a bit too much up the square
    except ZeroDivisionError:
        time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        #print(time1)
        #print(time2)
        return
    except IndexError:
        time2 = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        #print(time1)
        #print(time2)
        return -1,-1
    #return results, decalage_x        
    
        
                                
            
if __name__ == '__main__':
    
    L = []
    true = 0
    none = 0
    file = open("coords_square.txt",'r')
    for line in file:
        coords = line.split("\n")[0].split(',')
        coords[0] = float(coords[0])
        coords[1] = float(coords[1])
        L.append(coords)
    #print(L)
    r = []
    for file in os.listdir("captcha"):
        if file.endswith(".txt"): 
            name = os.path.join("captcha/", file)
            square = squareFinding(name)
            print(square)
            print(name)
        #if not square is None:
            #if almostEgalPoint(square,L[i-1],10):
                #print(True,i)
                #true += 1
            #else:
                #print(False,i)
                #pass
        #else:
            #none += 1
    #print(true,len(L),none)
    #print(true/len(L))
        #print(i)
        #print('')
        #print('')
    
    #removeDuplicatesFromSquare()
    #print(squareFinding("square/1.txt"))
    #captchaPath = "captcha/19.txt"
    #ExtractCaptchaFromFile(captchaPath)
    


