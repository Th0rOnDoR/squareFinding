import os
from operator import itemgetter
from math import sqrt
#from tabulate import tabulate
import datetime

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
    names = []
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
            names.append(name)
    return results,names

def removeDuplicatesFromSquare():
    list_squares,names = GetSquares()
    index = []
    i = 0
    r = []
    for i in range(len(list_squares)):
        if list_squares[i] not in r:
            r.append(list_squares[i])
        else:
            print(names[i])
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
    '''
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
    '''
    removeDuplicatesFromSquare()
    #print(squareFinding("square/1.txt"))
    #captchaPath = "captcha/19.txt"
    #ExtractCaptchaFromFile(captchaPath)
    

